import SwiftUI
import UIKit

/// The single screen of the app: a localized prompt and two big pill buttons.
///
/// All user-facing text is pulled from `Localizable.xcstrings`. Layout direction
/// (including the right-to-left flip for Arabic and Persian) is handled
/// automatically by SwiftUI based on the active locale, so there is nothing
/// RTL-specific to do here.
struct ContentView: View {
    /// The localized word the user just chose, or `nil` before any tap.
    @State private var choice: LocalizedStringKey?

    var body: some View {
        VStack(spacing: 40) {
            Spacer()

            // Shows the prompt until a choice is made, then the chosen word large.
            Text(choice ?? "Tap to decide")
                .font(.system(size: choice == nil ? 28 : 80,
                              weight: .bold,
                              design: .rounded))
                .foregroundStyle(choice == nil ? .secondary : .primary)
                .multilineTextAlignment(.center)
                .contentTransition(.opacity)
                .animation(.snappy, value: stateID)
                .padding(.horizontal, 24)

            Spacer()

            VStack(spacing: 16) {
                DecisionButton(title: "Yes", color: .green) { choose("Yes") }
                DecisionButton(title: "No", color: .red) { choose("No") }
            }
            .padding(.horizontal, 24)
            .padding(.bottom, 32)
        }
    }

    /// Drives the prompt/result animation. `LocalizedStringKey` isn't `Equatable`
    /// in a way we can animate on directly, so we animate on a derived flag.
    private var stateID: Bool { choice != nil }

    private func choose(_ value: LocalizedStringKey) {
        UIImpactFeedbackGenerator(style: .medium).impactOccurred()
        choice = value
    }
}

/// A full-width rounded "pill" button with a press scale/opacity animation.
private struct DecisionButton: View {
    let title: LocalizedStringKey
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 32, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 22)
                .background(color, in: Capsule())
        }
        .buttonStyle(PressStyle())
    }
}

/// Press feedback shared by both buttons.
private struct PressStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(.spring(response: 0.3, dampingFraction: 0.6),
                       value: configuration.isPressed)
    }
}

#Preview {
    ContentView()
}
