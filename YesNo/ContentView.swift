import SwiftUI
import UIKit

extension Color {
    /// Softened "yes" green (#5FC689) — gentler than the vivid system green.
    static let yesGreen = Color(red: 95 / 255, green: 198 / 255, blue: 137 / 255)
    /// Softened "no" red (#F26B62).
    static let noRed = Color(red: 242 / 255, green: 107 / 255, blue: 98 / 255)
}

/// The single screen of the app: two full-screen buttons split top/bottom —
/// a green **Yes** filling the upper half and a red **No** filling the lower
/// half. Tapping a half plays that button's sound, fires haptic feedback, and
/// animates the press.
///
/// All user-facing text comes from `Localizable.xcstrings`. Layout direction
/// (including the right-to-left flip for Arabic and Persian) is handled
/// automatically by SwiftUI based on the active locale.
struct ContentView: View {
    /// Whether the user has tapped yet — used to hide the prompt after the
    /// first choice.
    @State private var hasChosen = false

    var body: some View {
        ZStack {
            VStack(spacing: 0) {
                HalfButton(title: "Yes", color: .yesGreen, sound: "yes") { choose() }
                HalfButton(title: "No", color: .noRed, sound: "no") { choose() }
            }
            .ignoresSafeArea()

            // A small prompt chip on the divider, shown until the first tap.
            if !hasChosen {
                Text("Tap to decide")
                    .font(.system(size: 17, weight: .semibold, design: .rounded))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 18)
                    .padding(.vertical, 10)
                    .background(.black.opacity(0.35), in: Capsule())
                    .allowsHitTesting(false)
                    .transition(.opacity)
            }
        }
        .animation(.easeOut(duration: 0.25), value: hasChosen)
    }

    private func choose() {
        if !hasChosen { hasChosen = true }
    }
}

/// One half of the screen: a solid color filling its space, a big centered
/// label, its own sound, haptic feedback, and a press animation.
private struct HalfButton: View {
    let title: LocalizedStringKey
    let color: Color
    let sound: String
    let onChoose: () -> Void

    var body: some View {
        Button {
            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
            SoundPlayer.shared.play(sound)
            onChoose()
        } label: {
            ZStack {
                color
                Text(title)
                    .font(.system(size: 96, weight: .heavy, design: .rounded))
                    .foregroundStyle(.white)
                    .minimumScaleFactor(0.5)
                    .lineLimit(1)
                    .padding(.horizontal, 24)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .contentShape(Rectangle())
        }
        .buttonStyle(HalfPressStyle())
    }
}

/// Darkens and slightly shrinks the tapped half while the finger is down.
private struct HalfPressStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .brightness(configuration.isPressed ? -0.08 : 0)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.spring(response: 0.25, dampingFraction: 0.7),
                       value: configuration.isPressed)
    }
}

#Preview {
    ContentView()
}
