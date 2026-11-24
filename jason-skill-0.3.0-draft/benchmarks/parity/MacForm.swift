import Foundation
import SwiftUI

@main
struct JasonParityApp: App {
    var body: some Scene {
        WindowGroup("Jason Skill Parity Test") {
            FormView().padding().frame(width: 460, height: 205)
        }
    }
}

struct FormView: View {
    @State private var name = ""
    @State private var enabled = false
    @State private var count = 0
    @State private var status = "Not saved"
    @State private var saved = false

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            TextField("Test text", text: $name)
            Toggle("Enable test", isOn: $enabled)
            HStack {
                Button("Add one") { count += 1 }
                Text("Count: \(count)")
            }
            Button("Save test", action: save).disabled(saved)
            Text(status)
        }
    }

    func save() {
        guard let path = CommandLine.arguments.dropFirst().first else {
            status = "Pass a fresh result path as an argument"
            return
        }
        do {
            let record: [String: Any] = ["name": name, "enabled": enabled, "count": count]
            let bytes = try JSONSerialization.data(withJSONObject: record)
            try bytes.write(to: URL(fileURLWithPath: path), options: .withoutOverwriting)
            status = "Saved: \(name) / \(enabled)"
            saved = true
        } catch {
            status = "Save failed. Choose a new writable result destination."
        }
    }
}
