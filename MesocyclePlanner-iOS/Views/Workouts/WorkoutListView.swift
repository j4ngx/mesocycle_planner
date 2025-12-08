//
//  WorkoutListView.swift
//  MesocyclePlanner
//

import SwiftUI

struct WorkoutListView: View {
    @State private var selectedDate = Date()
    
    var body: some View {
        NavigationStack {
            VStack {
                // Calendar view placeholder
                Text("Workout Calendar")
                    .font(AppTypography.title)
                
                Text("Coming soon: Calendar view with scheduled workouts")
                    .font(AppTypography.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding()
            }
            .navigationTitle("Workouts")
        }
    }
}
