// frontend/mock/mockData.js

export const mockUserProfile = {
  name: "Ellen Ripley",
  pronouns: "she/her",
  location: "USCSS Nostromo (formerly)",
  birth_date: "2092-01-07",
  profile_description: "Warrant Officer. Xenomorph eliminator. Feline mom to Jonesy.",
  languages_spoken: "English, Binary",
  experience_with: "Deep space survival, synthetic allies, PTSD management",
  public_fields: ["location", "experience_with", "profile_description"],
};

export const mockPetProfiles = [
  {
    id: 1,
    name: "Jonesy",
    birthday: "2120-03-15",
    species: "Cat",
    subspecies: "Orange Tabby",
    gender: "Male",
    profile_description: "Space veteran. Sleeps through alien attacks. Purrs like thunder.",
    data: {
      favorite_things: "Warm engines, tuna packs, hiding in ducts",
      dislikes: "Facehuggers, loud alarms",
      social_style: "Solo operator",
      communication: "Telepathic judgment stares",
      preferred_treats: "Freeze-dried mice",
      diet: "Nutrient paste + synthetic meat blend",
      allergies: "Cryo-pod lubricant (minor reaction)",
      medical_alerts: "Monitor stress levels post-hyperjump",
      behavior_notes: "Scratches when scanned by androids",
      additional_info: "Immunized before LV-426 mission",
    },
    medical: {
      blood_type: "A+",
      weight: "4.2 kg",
      chronic_conditions: "Hypersleep disorientation",
      notes: "Keep crate open during landings to reduce panic",
      vaccinations: [
        {
          vaccine_name: "Feline Space Virus VX-4",
          dose_number: 2,
          batch_number: "FSV4-22B",
          previous_vaccination_date: "2123-04-01",
          next_vaccination_date: "2124-04-01",
          additional_info: "Required for interstellar travel",
        },
      ],
      medications: [
        {
          name: "Neurocalm Gel",
          dosage: "1 capsule/day",
          duration: "2 weeks post-hyperjump",
          additional_info: "Administer in tuna for stealth delivery",
        },
      ],
      tests: [
        {
          test_type: "Cognitive Response Scan",
          result: "Stable, reactive to crew stress levels",
          test_date: "2123-11-20",
          additional_info: "High empathy markers detected",
        },
      ],
    },
  },
];
