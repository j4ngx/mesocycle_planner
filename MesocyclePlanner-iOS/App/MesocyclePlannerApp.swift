//
//  MesocyclePlannerApp.swift
//  MesocyclePlanner
//
//  Main app entry point
//

import SwiftUI

@main
struct MesocyclePlannerApp: App {
    @StateObject private var authService = AuthService.shared
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authService)
                .environmentObject(appState)
                .preferredColorScheme(appState.colorScheme)
        }
    }
}

// MARK: - App State
class AppState: ObservableObject {
    @Published var colorScheme: ColorScheme?
    @Published var selectedTab: Tab = .home
    
    enum Tab {
        case home
        case exercises
        case mesocycles
        case workouts
        case profile
    }
}
