[app]
title = Hill Climb Racing
package.name = hillclimbracing
package.domain = org.hillclimb
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = landscape
fullscreen = 1
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.sdk_build_tools_version = 33.0.2
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
