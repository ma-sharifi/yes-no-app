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

## Automated publishing via GitHub Actions (no Mac needed by you)

This repo includes a working CI pipeline that builds, signs, and uploads the
app to App Store Connect from a GitHub-hosted **macOS runner**:

- `.github/workflows/deploy-appstore.yml` — runs on `workflow_dispatch` (the
  Actions tab) or when you push a `v*` tag.
- `fastlane/Fastfile` — the `release` lane that builds and uploads.

You never touch a Mac; you only provide credentials **once**, as encrypted
GitHub repo secrets. The pipeline uploads the binary to App Store Connect,
where it appears in TestFlight; you then click **Submit for Review** in the
App Store Connect UI (step 6 above) — Apple requires that final action to be
done by a human under your account.

### One-time setup

1. **Apple Developer account** + an app record created in App Store Connect
   (steps 0–2 above), using a bundle id you own. Update `app_identifier` in
   `fastlane/Appfile` and `PRODUCT_BUNDLE_IDENTIFIER` if you change it.

2. **App Store Connect API key** — App Store Connect → Users and Access →
   **Integrations / Keys** → generate a key with **App Manager** access.
   Download the `.p8` once.

3. **Distribution certificate** — export your Apple Distribution certificate
   (with its private key) from Keychain Access as a `.p12` with a password.
   (If you don't have one, create it at developer.apple.com → Certificates.)

4. **Add repo secrets** — GitHub repo → Settings → Secrets and variables →
   Actions → **New repository secret**, for each of:

   | Secret | Value |
   | --- | --- |
   | `ASC_KEY_ID` | The API key's Key ID |
   | `ASC_ISSUER_ID` | The API key's Issuer ID |
   | `ASC_KEY_CONTENT` | The `.p8` file contents, base64-encoded: `base64 -i AuthKey_XXX.p8 \| pbcopy` |
   | `BUILD_CERTIFICATE_BASE64` | The `.p12`, base64-encoded: `base64 -i cert.p12 \| pbcopy` |
   | `P12_PASSWORD` | The password you set when exporting the `.p12` |
   | `KEYCHAIN_PASSWORD` | Any string — a temporary keychain password for the runner |
   | `DEVELOPMENT_TEAM` | Your 10-character Team ID |

### Run it

- GitHub → **Actions** → **Deploy to App Store** → **Run workflow**, or
- `git tag v1.0.0 && git push origin v1.0.0`.

The build lands in TestFlight within a few minutes of the run finishing. From
App Store Connect you can test it, attach it to your App Store version, and
submit for review.

> Want to run it locally on a Mac instead? Set the same values as environment
> variables and run `fastlane release` from the repo root.
