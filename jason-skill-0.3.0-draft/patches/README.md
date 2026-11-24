# Optional local Cua 0.55.0 compatibility patch

This source-only patch was developed against upstream Cua tag `cua-driver-rs-v0.55.0`, commit prefix `8f484f3`. It disables a private raw SkyLight event-record path on macOS 14 and unknown versions, preserving the driver's available semantic fallbacks. A local Intel macOS 14.8.9 build passed the synthetic native form and saved-output check.

The public installer continues to fetch the official signed upstream release. This patch is for users who choose to build their own compatibility version and validate it. It carries no Apple signing identity, system permissions, browser profile, or publisher configuration.

Apply from the checked-out upstream root with `git apply /path/to/cua-0.55.0-sonoma.patch`, then follow that revision's documented build prerequisites and commands under `libs/cua-driver/rust`. Run the included compatibility test and the shared acceptance fixtures before selecting the build for actual work.

Upstream Cua Driver declares the MIT license. Jason Skill's changes are also MIT licensed. Reported related issue: https://github.com/trycua/cua/issues/2688
