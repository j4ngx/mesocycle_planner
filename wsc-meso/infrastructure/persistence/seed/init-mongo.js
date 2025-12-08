// MongoDB initialization script
// This script will be executed when the container starts for the first time

db = db.getSiblingDB('mesocycle_planner');

// Create collections
db.createCollection('users');
db.createCollection('exercises');
db.createCollection('mesocycles');
db.createCollection('workouts');
db.createCollection('progress');

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "username": 1 }, { unique: true });
db.exercises.createIndex({ "muscle_group": 1 });
db.exercises.createIndex({ "type": 1 });
db.exercises.createIndex({ "name": "text", "execution": "text" });
db.mesocycles.createIndex({ "user_id": 1 });
db.mesocycles.createIndex({ "user_id": 1, "status": 1 });
db.workouts.createIndex({ "mesocycle_id": 1 });
db.workouts.createIndex({ "mesocycle_id": 1, "completed": 1 });
db.workouts.createIndex({ "scheduled_date": 1 });
db.progress.createIndex({ "user_id": 1, "metric_type": 1 });
db.progress.createIndex({ "user_id": 1, "date": -1 });

print('✅ Database and indexes created successfully');

// Insert exercises - PECTORALS
let exerciseId = 1;
const pectoralExercises = [
    "Press de banca",
    "Press de banca manos juntas (agarre cerrado)",
    "Press de banca manos separadas (agarre abierto)",
    "Press de banca manos juntas y codos pegados",
    "Press de banca inclinado",
    "Press de banca inclinado con mancuernas",
    "Press de banca inclinado con mancuernas y giro hacia fuera",
    "Press de banca declinado",
    "Press de banca declinado con mancuernas",
    "Press de banca declinado con mancuernas y giro hacia fuera",
    "Press con mancuernas",
    "Press con mancuernas con giro hacia fuera",
    "Press con mancuernas con palmas enfrentadas",
    "Aperturas (aberturas con mancuernas)",
    "Aperturas inclinadas",
    "Aperturas declinadas",
    "Aperturas cruzando",
    "Fondos en el suelo",
    "Fondos pies en alto",
    "Fondos manos en alto",
    "Fondos en la pared",
    "Fondos con codos rectos",
    "Fondos en paralelas",
    "Fondos con lastre",
    "Fondos cuerpo recto",
    "Pull over con mancuerna",
    "Pull over con barra",
    "Pull over banco cruzado",
    "Pull over a dos manos alterno",
    "Giros con mancuernas",
    "Fondos rodando con mancuernas",
    "Elevaciones de barra lateral a una mano",
    "Press de banca con codos rectos",
    "Pull over sobre mancuernas en el suelo",
    "Press de banca en máquina",
    "Press de banca en máquina inclinado",
    "Press de banca en máquina declinado",
    "Press de banca en máquina sentado vertical",
    "Press de banca en multipower",
    "Press de banca en multipower inclinado",
    "Press de banca en multipower declinado",
    "Press de banca en multipower codos rectos",
    "Cruce de poleas",
    "Cruce de poleas tipo press",
    "Cruce de poleas a una mano",
    "Cruce de poleas a una mano en polea baja",
    "Aperturas en poleas bajas",
    "Aperturas en poleas bajas inclinado",
    "Aperturas en poleas bajas tipo press",
    "Aperturas en poleas bajas a una mano",
    "Contractor",
    "Contractor brazos abiertos",
    "Contractor solo movimiento final",
    "Pull over en polea baja",
    "Fondos en paralelas con ayuda"
];

pectoralExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "pectorals",
        type: name.includes("máquina") ? "machine" :
            name.includes("polea") || name.includes("poleas") ? "cable" :
                name.includes("multipower") ? "smith_machine" :
                    name.includes("mancuerna") || name.includes("barra") || name.includes("disco") ? "free_weight" :
                        "bodyweight",
        primary_muscles: ["pectoralis_major"],
        secondary_muscles: ["triceps", "anterior_deltoid"],
        antagonist_muscles: ["latissimus_dorsi"],
        execution: `Ejercicio de pectoral: ${name}`,
        comments: "Ejercicio para desarrollo de pectorales",
        common_mistakes: ["Arquear excesivamente la espalda", "Bloquear completamente los codos"],
        variants: [],
        difficulty: "intermediate",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - BACK (DORSAL)
const backExercises = [
    "Dominadas",
    "Dominadas tras nuca",
    "Dominadas en supinación (para bíceps)",
    "Dominadas en escalera (agarre neutro a dos lados alterno)",
    "Dominadas barra a la cintura",
    "Dominadas en barra baja y apoyo de pies",
    "Remo con barra",
    "Remo con mancuernas",
    "Remo en supinación",
    "Remo con mancuernas y agarre estrecho",
    "Remo sobre banco",
    "Remo con barra T",
    "Remo en punta",
    "Remo en punta abierto",
    "Remo en punta a una mano",
    "Remo con mancuerna",
    "Remo con mancuerna abierto",
    "Remo con mancuerna cuerpo elevado",
    "Remo con mancuerna extensiones brazos rectos",
    "Pull over con mancuerna",
    "Pull over con dos mancuernas alterno",
    "Pull over banco cruzado",
    "Pull over con barra",
    "Tracción a una mano lateral",
    "Extensiones de brazos rectos con barra",
    "Máquina de dorsal (jalón en máquina)",
    "Jalón en máquina a una mano en palanca",
    "Jalón en máquina a una mano y parada abajo",
    "Jalón polea al pecho",
    "Jalón polea tras nuca",
    "Jalón polea invertido en supinación",
    "Jalón polea agarre estrecho",
    "Jalón polea tumbado",
    "Jalón polea agarre neutro barra T",
    "Remo en polea Gironda",
    "Remo en polea agarre abierto",
    "Remo en polea polea alta",
    "Remo en polea a una mano",
    "Remo en polea agarre neutro barra T",
    "Remo en máquina",
    "Remo en máquina abierto",
    "Remo en máquina a una mano",
    "Remo de pie en polea baja",
    "Remo de pie en polea alta",
    "Remo de pie a una mano",
    "Remo de pie en supinación",
    "Pull over en polea alta",
    "Pull over en polea alta con cuerda",
    "Pull over en polea alta en máquina sentado",
    "Dominadas en máquina con ayuda",
    "Dominadas en máquina agarre neutro",
    "Dominadas en máquina a una mano",
    "Jalón a una mano",
    "Jalón a una mano sentado en el suelo",
    "Jalón a una mano sentado de lado",
    "Cruce de poleas por la espalda",
    "Aducción de codos en máquina",
    "Remo en multipower",
    "Remo en máquina vertical"
];

backExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "back",
        type: name.includes("máquina") ? "machine" :
            name.includes("polea") || name.includes("poleas") || name.includes("Jalón") ? "cable" :
                name.includes("multipower") ? "smith_machine" :
                    name.includes("mancuerna") || name.includes("barra") ? "free_weight" :
                        "bodyweight",
        primary_muscles: ["latissimus_dorsi", "trapezius"],
        secondary_muscles: ["biceps", "posterior_deltoid"],
        antagonist_muscles: ["pectoralis_major"],
        execution: `Ejercicio de espalda: ${name}`,
        comments: "Ejercicio para desarrollo de dorsales",
        common_mistakes: ["Usar impulso excesivo", "No completar el rango de movimiento"],
        variants: [],
        difficulty: "intermediate",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - SHOULDERS (HOMBRO)
const shoulderExercises = [
    "Press militar frontal con barra",
    "Press militar tras nuca",
    "Press militar agarre estrecho y codos al frente",
    "Press con mancuernas",
    "Press con mancuernas de pie",
    "Press con mancuernas a una mano",
    "Press con mancuernas a dos manos con parada arriba",
    "Press con mancuernas palmas enfrentadas",
    "Press con mancuernas tipo W",
    "Press frontal con mancuernas",
    "Press frontal banco inclinado",
    "Press frontal con giro (press Arnold/Scott)",
    "Elevaciones laterales con mancuernas",
    "Elevaciones laterales pulgares hacia arriba",
    "Elevaciones laterales pulgares hacia abajo",
    "Elevaciones laterales elevaciones completas",
    "Elevaciones laterales extensiones en cruz directas",
    "Elevaciones laterales a una mano",
    "Elevaciones laterales a una mano cuerpo inclinado",
    "Elevaciones frontales (flexiones con mancuernas)",
    "Elevaciones frontales simultáneo a dos manos",
    "Elevaciones frontales con manos en posición neutra (martillo)",
    "Elevaciones frontales con barra",
    "Elevaciones frontales con disco/mancuerna",
    "Elevaciones posteriores (pájaros de pie)",
    "Elevaciones posteriores sentado",
    "Elevaciones posteriores recostado sobre un banco",
    "Elevaciones posteriores recostado a una mano",
    "Elevaciones posteriores tumbado sobre codos elevando tronco",
    "Elevaciones posteriores tumbado lateral (abducción horizontal tumbado)",
    "Elevaciones posteriores codo cercano al cuerpo",
    "Elevaciones posteriores extensiones de brazos rectos",
    "Remo al cuello con barra",
    "Remo al cuello con mancuernas",
    "Remo al cuello con barra y extensión al frente",
    "Remo al cuello tronco flexionado",
    "Elevaciones (encogimientos de hombros con mancuernas)",
    "Elevaciones con giro",
    "Elevaciones con barra",
    "Elevaciones cuerpo flexionado",
    "Rotaciones externas tumbado",
    "Rotaciones internas tumbado",
    "Flexiones de hombro en banco con codos bloqueados",
    "Fondos en vertical invertido",
    "Elevaciones frontales inclinado",
    "Depresión de hombros en paralelas",
    "Extensiones de cabeza tumbado",
    "Inclinaciones laterales de cabeza tumbado",
    "Flexiones de cabeza tumbado",
    "Giros de cabeza",
    "Press en máquina",
    "Press en máquina agarre frontal",
    "Press en máquina sentado entre poleas bajas",
    "Press frontal militar en multipower",
    "Press frontal militar en multipower tras nuca",
    "Press frontal militar en multipower agarre estrecho y codos al frente",
    "Elevaciones laterales en máquina",
    "Elevaciones laterales en máquina a una mano",
    "Elevaciones laterales en máquina inclinado",
    "Elevaciones laterales en polea baja a una mano",
    "Elevaciones laterales en polea baja por detrás",
    "Elevaciones laterales en polea baja cruzando a dos manos",
    "Elevaciones frontales en polea baja",
    "Elevaciones frontales en polea baja a dos manos con cuerda/barra"
];

shoulderExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "shoulders",
        type: name.includes("máquina") ? "machine" :
            name.includes("polea") || name.includes("poleas") ? "cable" :
                name.includes("multipower") ? "smith_machine" :
                    name.includes("mancuerna") || name.includes("barra") || name.includes("disco") ? "free_weight" :
                        "bodyweight",
        primary_muscles: ["deltoid"],
        secondary_muscles: ["trapezius", "triceps"],
        antagonist_muscles: ["latissimus_dorsi"],
        execution: `Ejercicio de hombros: ${name}`,
        comments: "Ejercicio para desarrollo de deltoides",
        common_mistakes: ["Usar impulso", "Elevar demasiado peso"],
        variants: [],
        difficulty: "intermediate",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - LEGS (PIERNAS)
const legExercises = [
    "Sentadilla con barra",
    "Sentadilla frontal",
    "Sentadilla búlgara",
    "Sentadilla sumo",
    "Sentadilla pistol (a una pierna)",
    "Sentadilla con salto",
    "Sentadilla hack",
    "Sentadilla en multipower",
    "Sentadilla en máquina",
    "Prensa de piernas",
    "Prensa de piernas a una pierna",
    "Prensa de piernas pies juntos",
    "Prensa de piernas pies separados",
    "Prensa de piernas pies altos",
    "Prensa de piernas pies bajos",
    "Zancadas con barra",
    "Zancadas con mancuernas",
    "Zancadas caminando",
    "Zancadas inversas",
    "Zancadas laterales",
    "Peso muerto",
    "Peso muerto rumano",
    "Peso muerto sumo",
    "Peso muerto a una pierna",
    "Peso muerto con mancuernas",
    "Buenos días",
    "Extensiones de cuádriceps en máquina",
    "Extensiones de cuádriceps a una pierna",
    "Curl femoral tumbado",
    "Curl femoral sentado",
    "Curl femoral de pie",
    "Curl femoral a una pierna",
    "Elevaciones de gemelos de pie",
    "Elevaciones de gemelos sentado",
    "Elevaciones de gemelos en prensa",
    "Elevaciones de gemelos a una pierna",
    "Elevaciones de gemelos en multipower",
    "Aductores en máquina",
    "Abductores en máquina",
    "Patada de glúteo en máquina",
    "Patada de glúteo con polea",
    "Puente de glúteos",
    "Puente de glúteos a una pierna",
    "Hip thrust con barra",
    "Hip thrust a una pierna",
    "Step ups con mancuernas",
    "Step ups con barra",
    "Saltos al cajón",
    "Sentadilla sissy",
    "Sentadilla Jefferson",
    "Sentadilla Zercher",
    "Farmer walk (caminata del granjero)",
    "Subidas al banco",
    "Desplantes estáticos",
    "Desplantes con salto",
    "Extensión de cadera en máquina",
    "Flexión de cadera en máquina",
    "Abducción de cadera tumbado",
    "Aducción de cadera tumbado",
    "Elevación de talones en escalón",
    "Sentadilla goblet con kettlebell",
    "Sentadilla overhead",
    "Sentadilla con pausa",
    "Sentadilla con cadenas",
    "Sentadilla con bandas elásticas"
];

legExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "legs",
        type: name.includes("máquina") || name.includes("Prensa") ? "machine" :
            name.includes("polea") ? "cable" :
                name.includes("multipower") ? "smith_machine" :
                    name.includes("mancuerna") || name.includes("barra") || name.includes("kettlebell") ? "free_weight" :
                        "bodyweight",
        primary_muscles: ["quadriceps", "hamstrings", "glutes"],
        secondary_muscles: ["calves", "core"],
        antagonist_muscles: [],
        execution: `Ejercicio de piernas: ${name}`,
        comments: "Ejercicio para desarrollo de piernas",
        common_mistakes: ["Rodillas hacia dentro", "No llegar a profundidad adecuada"],
        variants: [],
        difficulty: "intermediate",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - BICEPS
const bicepsExercises = [
    "Curl con barra",
    "Curl con barra Z",
    "Curl con mancuernas",
    "Curl martillo",
    "Curl concentrado",
    "Curl predicador",
    "Curl en banco inclinado",
    "Curl 21s",
    "Curl en polea baja",
    "Curl en polea alta",
    "Curl araña (spider curl)"
];

bicepsExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "biceps",
        type: name.includes("polea") ? "cable" :
            name.includes("mancuerna") || name.includes("barra") ? "free_weight" :
                "machine",
        primary_muscles: ["biceps_brachii"],
        secondary_muscles: ["brachialis", "brachioradialis"],
        antagonist_muscles: ["triceps"],
        execution: `Ejercicio de bíceps: ${name}`,
        comments: "Ejercicio para desarrollo de bíceps",
        common_mistakes: ["Usar impulso", "Mover los codos"],
        variants: [],
        difficulty: "beginner",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - TRICEPS
const tricepsExercises = [
    "Press francés",
    "Press francés con mancuernas",
    "Extensiones sobre la cabeza",
    "Extensiones en polea alta",
    "Extensiones en polea con cuerda",
    "Patada de tríceps",
    "Fondos en paralelas para tríceps",
    "Press cerrado",
    "Extensiones tumbado (skullcrushers)",
    "Extensiones a una mano"
];

tricepsExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "triceps",
        type: name.includes("polea") ? "cable" :
            name.includes("mancuerna") || name.includes("barra") ? "free_weight" :
                "bodyweight",
        primary_muscles: ["triceps"],
        secondary_muscles: [],
        antagonist_muscles: ["biceps"],
        execution: `Ejercicio de tríceps: ${name}`,
        comments: "Ejercicio para desarrollo de tríceps",
        common_mistakes: ["Mover los codos", "Arquear la espalda"],
        variants: [],
        difficulty: "beginner",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - ABS
const absExercises = [
    "Crunch abdominal",
    "Crunch inverso",
    "Plancha frontal",
    "Plancha lateral",
    "Elevaciones de piernas",
    "Bicicleta abdominal",
    "Mountain climbers",
    "Russian twist",
    "Ab wheel rollout",
    "Crunch en polea alta",
    "Elevaciones de rodillas colgado",
    "L-sit",
    "Dragon flag",
    "Plancha con elevación de pierna",
    "Dead bug"
];

absExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "abs",
        type: name.includes("polea") ? "cable" :
            name.includes("wheel") ? "other" :
                "bodyweight",
        primary_muscles: ["rectus_abdominis", "obliques"],
        secondary_muscles: ["transverse_abdominis"],
        antagonist_muscles: ["erector_spinae"],
        execution: `Ejercicio de abdominales: ${name}`,
        comments: "Ejercicio para desarrollo de core",
        common_mistakes: ["Tirar del cuello", "No contraer el abdomen"],
        variants: [],
        difficulty: "beginner",
        created_at: new Date(),
        updated_at: new Date()
    });
});

// Insert exercises - FOREARMS
const forearmExercises = [
    "Curl de muñeca con barra",
    "Curl de muñeca inverso",
    "Curl de muñeca con mancuernas",
    "Farmer walk",
    "Agarre con pinza",
    "Rotación de muñeca con mancuerna"
];

forearmExercises.forEach(name => {
    db.exercises.insertOne({
        _id: exerciseId++,
        name: name,
        number: String(exerciseId - 1),
        muscle_group: "forearms",
        type: name.includes("mancuerna") || name.includes("barra") ? "free_weight" : "other",
        primary_muscles: ["forearm_flexors", "forearm_extensors"],
        secondary_muscles: [],
        antagonist_muscles: [],
        execution: `Ejercicio de antebrazos: ${name}`,
        comments: "Ejercicio para desarrollo de antebrazos",
        common_mistakes: ["Usar demasiado peso", "Movimiento incompleto"],
        variants: [],
        difficulty: "beginner",
        created_at: new Date(),
        updated_at: new Date()
    });
});

print(`✅ Inserted ${exerciseId - 1} exercises successfully`);
print('✅ Database initialization completed!');
