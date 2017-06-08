# Cipher非线程安全


Cipher非线程安全，在实现工具类的时候要注意这点，可以使用局部变量或者ThreadLocal。SimpleDateFormat类似。

测试代码如下：

```java
public static void main(String[] args) throws Exception {
    File privateFile = new File(RSAEncryptUtil.class.getClassLoader().getResource("KeyPair/private.pem").getFile());
    File pubFile = new File(RSAEncryptUtil.class.getClassLoader().getResource("KeyPair/public.pem").getFile());
    PrivateKey priv = createPrivate(privateFile);
    PublicKey pub = createPublic(pubFile);
    for (int j = 0; j < 10; j++) {
        for (int i = 0; i < 10; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String msg = "hello world aaaaabbbbbbb";
                        String enct = RSAEncryptUtil.encryptText(msg, priv);
                        String dect = RSAEncryptUtil.decryptText(enct, pub);
                        if (!StringUtils.equals(msg, dect)) {
                            System.out.println("BROKEN");
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }).start();
        }
    }
}
```



情况1，Cipher是静态变量时：

```java
public static String encryptText1(String msg, Key key) throws NoSuchAlgorithmException, NoSuchPaddingException,
                    UnsupportedEncodingException, IllegalBlockSizeException, BadPaddingException, InvalidKeyException {
        CIPHER.init(Cipher.ENCRYPT_MODE, key); // 这里1
        byte[] encrypted = CIPHER.doFinal(msg.getBytes("UTF-8"));
        return Base64.encodeBase64String(encrypted);
    }

    public static String decryptText1(String msg, Key key) {
        String res = "";
        try {
            CIPHER.init(Cipher.DECRYPT_MODE, key);
            res = new String(CIPHER.doFinal(Base64.decodeBase64(msg)), "UTF-8");
        } catch (Exception e) {
            logger.error(String.format("RSA解密失败, msg = %s", msg), e);
        }
        return res;
    }
```

很容易发生异常：

```java
BROKEN
19:41:15.876 [Thread-98] ERROR com.netease.is.cloudsafe.base.utils.rsa.RSAEncryptUtil - RSA解密失败, msg = q8BzDMchysw1Et1NVuG5srsbFk6c5kbMmy72FztiZ1JI3LTnfvoVDkgIJcZwYxi8vsDrl1oG09i6JGHS5qeAt9Y+rlRBhk/yBfYlkInFchUFprc2X52YXeJDw6x1DUY+/k2HObQNJIRDLUbYeVWG4eXBFfPSkQaNR4g9wetrob4=
javax.crypto.IllegalBlockSizeException: Data must not be longer than 128 bytes
	at com.sun.crypto.provider.RSACipher.doFinal(RSACipher.java:344)
	at com.sun.crypto.provider.RSACipher.engineDoFinal(RSACipher.java:389)
	at javax.crypto.Cipher.doFinal(Cipher.java:2165)
	at com.netease.is.cloudsafe.base.utils.rsa.RSAEncryptUtil.decryptText1(RSAEncryptUtil.java:177)
	at com.netease.is.cloudsafe.base.utils.rsa.RSAEncryptUtil$1.run(RSAEncryptUtil.java:207)
	at java.lang.Thread.run(Thread.java:745)
```


情况2，Cipher是局部成员变量时：

```java
public static String encryptText(String msg, Key key) throws NoSuchAlgorithmException, NoSuchPaddingException,
                UnsupportedEncodingException, IllegalBlockSizeException, BadPaddingException, InvalidKeyException {
    Cipher cipher = Cipher.getInstance("RSA"); // 这里2
    cipher.init(Cipher.ENCRYPT_MODE, key);
    byte[] encrypted = cipher.doFinal(msg.getBytes("UTF-8"));
    return Base64.encodeBase64String(encrypted);
}

public static String decryptText(String msg, Key key) {
    String res = "";
    try {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, key);
        res = new String(cipher.doFinal(Base64.decodeBase64(msg)), "UTF-8");
    } catch (Exception e) {
        logger.error(String.format("RSA解密失败, msg = %s", msg), e);
    }
    return res;
}
```

不会出现问题。
