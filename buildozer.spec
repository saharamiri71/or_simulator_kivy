[app]
title = OR Simulator
package.name = orsimulator
package.domain = org.kivy

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b

android.enable_androidx = True
android.enable_jetifier = True

android.permissions =
    INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
