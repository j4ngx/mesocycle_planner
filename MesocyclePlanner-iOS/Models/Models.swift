//
//  Models.swift
//  MesocyclePlanner
//
//  All data models matching OpenAPI specification
//

import Foundation

// MARK: - User Models
struct User: Codable, Identifiable {
    let id: UUID
    let email: String
    let username: String
    var fullName: String?
    var trainingLevel: TrainingLevel
    let createdAt: Date
    let updatedAt: Date
}

struct UserCreate: Codable {
    let email: String
    let username: String
    let password: String
    var fullName: String?
    var trainingLevel: TrainingLevel?
}

struct UserLogin: Codable {
    let email: String
    let password: String
}

struct TokenResponse: Codable {
    let accessToken: String
    let tokenType: String
}

enum TrainingLevel: String, Codable, CaseIterable {
    case beginner
    case intermediate
    case advanced
    case elite
    
    var displayName: String {
        rawValue.capitalized
    }
}

// MARK: - Exercise Models
struct Exercise: Codable, Identifiable {
    let id: Int
    let name: String
    let number: String
    let muscleGroup: MuscleGroup
    let type: ExerciseType
    let primaryMuscles: [String]
    var secondaryMuscles: [String]?
    var antagonistMuscles: [String]?
    var execution: String?
    var comments: String?
    var commonMistakes: [String]?
    var variants: [String]?
    var pdfPage: Int?
    var difficulty: String?
}

enum MuscleGroup: String, Codable, CaseIterable {
    case pectorals, back, shoulders, biceps, triceps, forearms, legs, abs
    
    var displayName: String {
        rawValue.capitalized
    }
    
    var icon: String {
        switch self {
        case .pectorals: return "figure.strengthtraining.traditional"
        case .back: return "figure.walk"
        case .shoulders: return "figure.arms.open"
        case .biceps: return "figure.strengthtraining.functional"
        case .triceps: return "figure.strengthtraining.functional"
        case .forearms: return "hand.raised"
        case .legs: return "figure.run"
        case .abs: return "figure.core.training"
        }
    }
}

enum ExerciseType: String, Codable, CaseIterable {
    case freeWeight = "free_weight"
    case machine
    case cable
    case smithMachine = "smith_machine"
    case bodyweight
    case other
    
    var displayName: String {
        switch self {
        case .freeWeight: return "Free Weight"
        case .machine: return "Machine"
        case .cable: return "Cable"
        case .smithMachine: return "Smith Machine"
        case .bodyweight: return "Bodyweight"
        case .other: return "Other"
        }
    }
}

// MARK: - Mesocycle Models
struct Mesocycle: Codable, Identifiable {
    let id: UUID
    let userId: UUID
    let name: String
    var description: String?
    let periodizationModel: PeriodizationModel
    let goal: TrainingGoal
    let durationWeeks: Int
    let startDate: Date
    let endDate: Date
    var status: MesocycleStatus
    let trainingLevel: String
    let weeklyFrequency: Int
    var deloadWeeks: [Int]?
    let createdAt: Date
    let updatedAt: Date
}

struct MesocycleCreate: Codable {
    let name: String
    var description: String?
    let periodizationModel: PeriodizationModel
    let goal: TrainingGoal
    let durationWeeks: Int
    let startDate: Date
    let endDate: Date
    let trainingLevel: String
    let weeklyFrequency: Int
    var deloadWeeks: [Int]?
}

enum PeriodizationModel: String, Codable, CaseIterable {
    case linear
    case dailyUndulating = "daily_undulating"
    case block
    case polarized
    
    var displayName: String {
        switch self {
        case .linear: return "Linear"
        case .dailyUndulating: return "DUP (Daily Undulating)"
        case .block: return "Block"
        case .polarized: return "Polarized"
        }
    }
}

enum TrainingGoal: String, Codable, CaseIterable {
    case strength, hypertrophy, power, endurance, definition
    
    var displayName: String {
        rawValue.capitalized
    }
    
    var icon: String {
        switch self {
        case .strength: return "bolt.fill"
        case .hypertrophy: return "figure.strengthtraining.traditional"
        case .power: return "flame.fill"
        case .endurance: return "figure.run"
        case .definition: return "star.fill"
        }
    }
}

enum MesocycleStatus: String, Codable {
    case planned, active, completed, paused
    
    var displayName: String {
        rawValue.capitalized
    }
    
    var color: String {
        switch self {
        case .planned: return "blue"
        case .active: return "green"
        case .completed: return "gray"
        case .paused: return "orange"
        }
    }
}

enum TrainingPhase: String, Codable {
    case accumulation, transmutation, realization, competition, deload
}

// MARK: - Workout Models
struct Workout: Codable, Identifiable {
    let id: UUID
    let mesocycleId: UUID
    var microcycleId: Int?
    let name: String
    var description: String?
    let scheduledDate: Date
    var completed: Bool
    var completedAt: Date?
    var durationMinutes: Int?
    var notes: String?
    var split: TrainingSplit?
    let createdAt: Date
    let updatedAt: Date
}

struct WorkoutCreate: Codable {
    let mesocycleId: UUID
    var microcycleId: Int?
    let name: String
    var description: String?
    let scheduledDate: Date
    var split: TrainingSplit?
    var notes: String?
}

enum TrainingSplit: String, Codable, CaseIterable {
    case push, pull, legs, fullbody, upper, lower
    
    var displayName: String {
        switch self {
        case .fullbody: return "Full Body"
        default: return rawValue.capitalized
        }
    }
}

// MARK: - Progress Models
struct Progress: Codable, Identifiable {
    let id: UUID
    let userId: UUID
    let date: Date
    let metricType: MetricType
    let value: Double
    var unit: String?
    var notes: String?
    let createdAt: Date
}

struct ProgressCreate: Codable {
    let date: Date
    let metricType: MetricType
    let value: Double
    var unit: String?
    var notes: String?
}

enum MetricType: String, Codable, CaseIterable {
    case weight, bodyFat = "body_fat", measurement, strength, endurance
    
    var displayName: String {
        switch self {
        case .weight: return "Weight"
        case .bodyFat: return "Body Fat %"
        case .measurement: return "Measurement"
        case .strength: return "Strength"
        case .endurance: return "Endurance"
        }
    }
    
    var defaultUnit: String {
        switch self {
        case .weight: return "kg"
        case .bodyFat: return "%"
        case .measurement: return "cm"
        case .strength: return "kg"
        case .endurance: return "min"
        }
    }
}
