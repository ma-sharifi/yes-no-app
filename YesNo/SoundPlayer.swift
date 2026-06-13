import AVFoundation

/// Plays the short per-button tap sounds bundled with the app
/// (`yes.wav` / `no.wav`).
///
/// Players are preloaded once and reused so taps are latency-free. The audio
/// session uses the `ambient` category, so sounds mix with other audio and
/// respect the hardware mute switch — the expected behavior for UI sound
/// effects.
final class SoundPlayer {
    static let shared = SoundPlayer()

    private var players: [String: AVAudioPlayer] = [:]

    private init() {
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.ambient, mode: .default, options: [.mixWithOthers])
        try? session.setActive(true)
        preload("yes")
        preload("no")
    }

    private func preload(_ name: String) {
        guard let url = Bundle.main.url(forResource: name, withExtension: "wav"),
              let player = try? AVAudioPlayer(contentsOf: url) else { return }
        player.prepareToPlay()
        players[name] = player
    }

    /// Plays the named sound from the start, restarting if already playing.
    func play(_ name: String) {
        guard let player = players[name] else { return }
        player.currentTime = 0
        player.play()
    }
}
