[app]
title = Pain Robot
package.name = painrobot
package.domain = org.pain
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 0.1
orientation = portrait
android.arch = arm64-v8a
requirements = python3,kivy,requests,pyjnius
android.permissions = CAMERA,RECORD_AUDIO,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE
android.manifest = ./templates/AndroidManifest.xml
android.minapi = 21
android.sdk = 28
android.ndk = 19b
log_level = 2
