[app]
title = Pain Robot
package.name = painrobot
package.domain = org.pain
source.include_exts = py,png,jpg,kv,txt
version = 0.1
orientation = portrait
android.arch = arm64-v8a
# Python version
requirements = python3,kivy,requests,pyjnius
# Permissions
android.permissions = CAMERA,RECORD_AUDIO,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE
# If you need USB host permission (some versions):
# android.permissions += android.permission.USB_PERMISSION

# launcher manifest template (we will provide a minimal template file merged by buildozer)
android.manifest = ./templates/AndroidManifest.xml

# (adjust these if needed)
android.minapi = 21
android.sdk = 28
android.ndk = 19b

# debug
log_level = 2
