import SwiftUI
import AppKit
@main struct SpeedTrial:App {
    var body:some Scene {WindowGroup("Background Control Test") {TrialView().frame(width:500,height:330)}}
}
struct TrialView:View {
    @State private var count=0
    @State private var name=""
    @State private var enabled=false
    @State private var saved="Not saved"
    @State private var revision=0
    var body:some View {
        VStack(alignment:.leading,spacing:12) {
            Text("Owned native control fixture").font(.headline)
            HStack {TextField("Test text",text:$name).accessibilityIdentifier("trial-name").id(revision);Toggle("Enable test",isOn:$enabled).toggleStyle(.checkbox)}
            Text("Text readback: \(name)")
            Text("Enabled: \(enabled ? "on" : "off")")
            Text("Count: \(count)")
            HStack {
                Button("Add one"){count+=1}
                Button("Save test"){saved="\(name)|\(enabled ? "on" : "off")"}
                Button("Reset form"){name="";enabled=false;saved="Not saved";revision+=1}
            }
            Text("Saved result: \(saved)").accessibilityIdentifier("trial-saved")
        }.padding(24)
    }
}
