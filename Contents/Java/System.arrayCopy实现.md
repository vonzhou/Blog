

往下细看，没有那么简单。

System.c

```c
static JNINativeMethod methods[] = {
    {"currentTimeMillis", "()J",              (void *)&JVM_CurrentTimeMillis},
    {"nanoTime",          "()J",              (void *)&JVM_NanoTime},
    {"arraycopy",     "(" OBJ "I" OBJ "II)V", (void *)&JVM_ArrayCopy},
};
```



jvm.cpp

```cpp
JVM_ENTRY(void, JVM_ArrayCopy(JNIEnv *env, jclass ignored, jobject src, jint src_pos,
                               jobject dst, jint dst_pos, jint length))
  JVMWrapper("JVM_ArrayCopy");
  // Check if we have null pointers
  if (src == NULL || dst == NULL) {
    THROW(vmSymbols::java_lang_NullPointerException());
  }
  arrayOop s = arrayOop(JNIHandles::resolve_non_null(src));
  arrayOop d = arrayOop(JNIHandles::resolve_non_null(dst));
  assert(s->is_oop(), "JVM_ArrayCopy: src not an oop");
  assert(d->is_oop(), "JVM_ArrayCopy: dst not an oop");
  // Do copy
  Klass::cast(s->klass())->copy_array(s, src_pos, d, dst_pos, length, thread);
JVM_END
```

objArrayKlass.cpp

```cpp
void objArrayKlass::copy_array(arrayOop s, int src_pos, arrayOop d,
                               int dst_pos, int length, TRAPS) {
  assert(s->is_objArray(), "must be obj array");

  if (!d->is_objArray()) {
    THROW(vmSymbols::java_lang_ArrayStoreException());
  }

  // Check is all offsets and lengths are non negative
  if (src_pos < 0 || dst_pos < 0 || length < 0) {
    THROW(vmSymbols::java_lang_ArrayIndexOutOfBoundsException());
  }
  // Check if the ranges are valid
  if  ( (((unsigned int) length + (unsigned int) src_pos) > (unsigned int) s->length())
     || (((unsigned int) length + (unsigned int) dst_pos) > (unsigned int) d->length()) ) {
    THROW(vmSymbols::java_lang_ArrayIndexOutOfBoundsException());
  }

  // Special case. Boundary cases must be checked first
  // This allows the following call: copy_array(s, s.length(), d.length(), 0).
  // This is correct, since the position is supposed to be an 'in between point', i.e., s.length(),
  // points to the right of the last element.
  if (length==0) {
    return;
  }
  if (UseCompressedOops) {
    narrowOop* const src = objArrayOop(s)->obj_at_addr<narrowOop>(src_pos);
    narrowOop* const dst = objArrayOop(d)->obj_at_addr<narrowOop>(dst_pos);
    do_copy<narrowOop>(s, src, d, dst, length, CHECK);
  } else {
    oop* const src = objArrayOop(s)->obj_at_addr<oop>(src_pos);
    oop* const dst = objArrayOop(d)->obj_at_addr<oop>(dst_pos);
    do_copy<oop> (s, src, d, dst, length, CHECK);
  }
}


template <class T> void objArrayKlass::do_copy(arrayOop s, T* src,
                               arrayOop d, T* dst, int length, TRAPS) {

  BarrierSet* bs = Universe::heap()->barrier_set();
  // For performance reasons, we assume we are that the write barrier we
  // are using has optimized modes for arrays of references.  At least one
  // of the asserts below will fail if this is not the case.
  assert(bs->has_write_ref_array_opt(), "Barrier set must have ref array opt");
  assert(bs->has_write_ref_array_pre_opt(), "For pre-barrier as well.");

  if (s == d) {
    // since source and destination are equal we do not need conversion checks.
    assert(length > 0, "sanity check");
    bs->write_ref_array_pre(dst, length);
    Copy::conjoint_oops_atomic(src, dst, length);
  } else {
    // We have to make sure all elements conform to the destination array
    klassOop bound = objArrayKlass::cast(d->klass())->element_klass();
    klassOop stype = objArrayKlass::cast(s->klass())->element_klass();
    if (stype == bound || Klass::cast(stype)->is_subtype_of(bound)) {
      // elements are guaranteed to be subtypes, so no check necessary
      bs->write_ref_array_pre(dst, length);
      Copy::conjoint_oops_atomic(src, dst, length);
    } else {
      // slow case: need individual subtype checks
      // note: don't use obj_at_put below because it includes a redundant store check
      T* from = src;
      T* end = from + length;
      for (T* p = dst; from < end; from++, p++) {
        // XXX this is going to be slow.
        T element = *from;
        // even slower now
        bool element_is_null = oopDesc::is_null(element);
        oop new_val = element_is_null ? oop(NULL)
                                      : oopDesc::decode_heap_oop_not_null(element);
        if (element_is_null ||
            Klass::cast((new_val->klass()))->is_subtype_of(bound)) {
          bs->write_ref_field_pre(p, new_val);
          *p = *from;
        } else {
          // We must do a barrier to cover the partial copy.
          const size_t pd = pointer_delta(p, dst, (size_t)heapOopSize);
          // pointer delta is scaled to number of elements (length field in
          // objArrayOop) which we assume is 32 bit.
          assert(pd == (size_t)(int)pd, "length field overflow");
          bs->write_ref_array((HeapWord*)dst, pd);
          THROW(vmSymbols::java_lang_ArrayStoreException());
          return;
        }
      }
    }
  }
  bs->write_ref_array((HeapWord*)dst, length);
}
```