# Deploying to the App Store

The actual upload must run on a **Mac with Xcode 16** and your **Apple
Developer account** — it can't be done from a Linux/CI box without your signing
credentials. This repo has everything else ready (code, localization, sounds,
1024px icon, bundle id). Here's the full path.

## 0. One-time prerequisites

- An [Apple Developer Program](https://developer.apple.com/programs/) membership
  ($99/year).
- Xcode 16+ signed in with your Apple ID (Xcode → Settings → Accounts).
- Your **Team ID** (App Store Connect → Membership → 10-character ID).

## 1. Set your team & bundle id

Open `YesNo.xcodeproj`, select the **YesNo** target → **Signing &
Capabilities**:

- Check **Automatically manage signing**.
- Pick your **Team**.
- Confirm the **Bundle Identifier**. It's `com.masharifi.YesNo` — if that's not
  registered to your team, change it to something you own (e.g.
  `com.yourname.YesNo`) here and in the project's build settings.

## 2. Create the app in App Store Connect

At [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → **Apps → +**:

- Platform: iOS
- Name: e.g. **Yes / No** (must be unique on the store)
- Primary language, bundle id (matches step 1), and an SKU (any string).

Fill in the listing: description, keywords, support URL, **privacy** (this app
collects **no data** — declare "Data Not Collected"), age rating, and category
(Utilities or Lifestyle).

## 3. Bump the version

In the target's build settings (or General tab):

- `MARKETING_VERSION` (e.g. `1.0`) — the public version.
- `CURRENT_PROJECT_VERSION` (e.g. `1`) — the build number; must increase with
  every upload.

## 4. Archive & upload

### Option A — Xcode GUI (simplest)

1. Set the run destination to **Any iOS Device (arm64)**.
2. **Product → Archive**.
3. In the Organizer that opens, select the archive → **Distribute App** →
   **App Store Connect** → **Upload**, and follow the prompts.

### Option B — command line

Edit `docs/ExportOptions.plist` and set `YOUR_TEAM_ID`, then:

```bash
xcodebuild -project YesNo.xcodeproj \
  -scheme YesNo \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath build/YesNo.xcarchive \
  archive

xcodebuild -exportArchive \
  -archivePath build/YesNo.xcarchive \
  -exportOptionsPlist docs/ExportOptions.plist \
  -exportPath build/export
```

This signs and uploads the build to App Store Connect.

## 5. Screenshots

App Store Connect requires real device screenshots (the images in
`docs/screenshots/` are design renders, not accepted for the listing). Capture
them from the Simulator (⌘S) at the required sizes — at minimum a 6.7"/6.9"
iPhone. Use the scheme's **App Language** option to grab localized sets if you
want per-language screenshots.

## 6. Submit for review

In App Store Connect, attach the uploaded build to the version, complete the
"App Review Information", and **Submit for Review**. Review typically takes a
day or two.

---

### Optional: automate with Fastlane

If you'll release often, [Fastlane](https://fastlane.tools) automates steps
3–4 and 6. A minimal `fastlane/Fastfile`:

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to App Store Connect"
  lane :release do
    increment_build_number(xcodeproj: "YesNo.xcodeproj")
    build_app(scheme: "YesNo")
    upload_to_app_store(submit_for_review: false)
  end
end
```

Run with `fastlane release` on your Mac (after `fastlane init`).
