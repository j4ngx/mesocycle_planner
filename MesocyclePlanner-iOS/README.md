# Mesocycle Planner iOS App

Professional iOS app built with SwiftUI for the Mesocycle Planner backend.

## Features

### ✅ Implemented
- **Authentication**: Login, register, secure token storage with Keychain
- **Exercise Library**: Browse 440+ exercises with search and muscle group filters
- **Exercise Details**: View execution instructions, muscles worked, common mistakes
- **Mesocycle Management**: Create and view training mesocycles
- **Profile**: User profile with logout functionality
- **Premium UI**: Modern design with gradients, cards, and smooth animations

### 🚧 In Progress
- Workout tracking and calendar
- Progress analytics with charts
- AI mesocycle generation
- Microcycle progression

## Architecture

- **Pattern**: MVVM (Model-View-ViewModel)
- **Networking**: URLSession with async/await
- **Storage**: Keychain (tokens), UserDefaults (preferences)
- **UI Framework**: SwiftUI
- **Minimum iOS**: 16.0

## Project Structure

```
MesocyclePlanner-iOS/
├── App/
│   ├── MesocyclePlannerApp.swift    # App entry point
│   └── ContentView.swift             # Root view with auth flow
├── Core/
│   ├── Networking/
│   │   └── APIClient.swift           # Generic API client
│   ├── Storage/
│   │   └── KeychainManager.swift     # Secure token storage
│   └── DesignSystem.swift            # Colors, typography, spacing
├── Models/
│   └── Models.swift                  # All data models
├── Services/
│   ├── AuthService.swift             # Authentication
│   ├── ExerciseService.swift         # Exercise operations
│   └── MesocycleService.swift        # Mesocycle operations
└── Views/
    ├── Auth/
    │   ├── LoginView.swift
    │   └── RegisterView.swift
    ├── Exercises/
    │   └── ExerciseLibraryView.swift
    ├── Mesocycles/
    │   └── MesocycleListView.swift
    ├── Workouts/
    │   └── WorkoutListView.swift
    ├── Profile/
    │   └── ProfileView.swift
    ├── Components/
    │   └── CustomComponents.swift
    └── MainTabView.swift
```

## Setup

### Prerequisites
- Xcode 15.0+
- iOS 16.0+
- Backend server running on `http://localhost:8000`

### Installation

1. Open the project in Xcode:
```bash
cd MesocyclePlanner-iOS
open MesocyclePlanner.xcodeproj
```

2. Update the API base URL in `APIClient.swift` if needed:
```swift
private let baseURL: String = "http://localhost:8000/api/v1"
```

3. Build and run (⌘R)

### Backend Setup

Make sure the backend server is running:
```bash
cd ../wsc-meso
docker compose up -d
source venv/bin/activate
PYTHONPATH=src:. uvicorn src.openapi_server.main:app --reload
```

## Usage

### Authentication
1. Launch the app
2. Tap "Sign up" to create an account
3. Or login with existing credentials

### Browse Exercises
1. Tap "Exercises" tab
2. Use search or filter by muscle group
3. Tap any exercise to view details

### Create Mesocycle
1. Tap "Mesocycles" tab
2. Tap the "+" button
3. Fill in the form and create

## API Integration

The app integrates with all backend endpoints:

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /users/me` - Get current user
- `GET /exercises` - List exercises
- `GET /exercises/search` - Search exercises
- `GET /mesocycles` - List mesocycles
- `POST /mesocycles` - Create mesocycle

## Design System

### Colors
- **Primary**: Blue gradient
- **Secondary**: Purple
- **Success**: Green
- **Warning**: Orange
- **Error**: Red

### Typography
- SF Pro Display (titles)
- SF Pro Text (body)
- Rounded design for modern feel

### Components
- Custom text fields with icons
- Gradient buttons
- Cards with shadows
- Filter chips
- Status badges

## Development

### Adding New Features

1. **Create Model** in `Models/Models.swift`
2. **Create Service** in `Services/`
3. **Create View** in `Views/`
4. **Update Navigation** in `MainTabView.swift`

### Code Style
- SwiftUI declarative syntax
- Async/await for networking
- ObservableObject for ViewModels
- Environment objects for dependency injection

## Testing

Run tests in Xcode:
```
⌘U
```

## Troubleshooting

### Cannot connect to backend
- Ensure backend is running on `http://localhost:8000`
- Check API base URL in `APIClient.swift`
- For simulator, use `http://localhost:8000`
- For device, use your computer's IP address

### Keychain errors
- Reset simulator: Device → Erase All Content and Settings

## Future Enhancements

- [ ] Workout timer with haptic feedback
- [ ] Progress charts with Swift Charts
- [ ] Offline mode with Core Data
- [ ] Apple Watch companion app
- [ ] HealthKit integration
- [ ] Push notifications for workouts
- [ ] Dark mode optimization
- [ ] Localization (Spanish, etc.)

## License

MIT License - See backend repository for details.
