<script setup>
import { ref, onMounted } from "vue";
import {
  getProfile,
  updateProfile,
  getMyPhotos,
  uploadPhotos,
  deletePhoto,
  setPrimaryPhoto,
  getInterests,
} from "../services/api";

const profile = ref({
  display_name: "",
  age: "",
  bio: "",
  location: "",
  gender: "",
  looking_for: "",
  visibility: "public",
  min_preferred_age: "",
  max_preferred_age: "",
  preferred_radius_km: "",
  profile_picture: "",
  interests: [],
});

const allInterests = ref([]);
const selectedInterests = ref([]);
const newInterest = ref("");
const photos = ref([]);
const message = ref("");
const errorMessage = ref("");
const loading = ref(false);
const dragActive = ref(false);

const imageUrl = (path) => {
  if (!path)
    return new URL("../assets/pics/default.webp", import.meta.url).href;
  return `http://localhost:5000${path}`;
};

const formatInterestName = (name) => {
  if (!name) return "";
  return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
};

const loadProfile = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [profileData, photosData, interestsData] = await Promise.all([
      getProfile(),
      getMyPhotos(),
      getInterests(),
    ]);

    profile.value = profileData;
    photos.value = photosData;
    allInterests.value = interestsData.map((item) => item.name);
    selectedInterests.value = (profileData.interests || []).map(
      (item) => item.name,
    );
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
};

const handleSave = async () => {
  message.value = "";
  errorMessage.value = "";

  try {
    if (selectedInterests.value.length < 3) {
      errorMessage.value = "Please choose at least 3 interests.";
      return;
    }

    const payload = {
      display_name: profile.value.display_name,
      age: profile.value.age === "" ? null : Number(profile.value.age),
      bio: profile.value.bio,
      location: profile.value.location,
      gender: profile.value.gender,
      looking_for: profile.value.looking_for,
      visibility: profile.value.visibility,
      min_preferred_age:
        profile.value.min_preferred_age === ""
          ? null
          : Number(profile.value.min_preferred_age),
      max_preferred_age:
        profile.value.max_preferred_age === ""
          ? null
          : Number(profile.value.max_preferred_age),
      preferred_radius_km:
        profile.value.preferred_radius_km === ""
          ? null
          : Number(profile.value.preferred_radius_km),
      interests: selectedInterests.value,
    };

    const result = await updateProfile(payload);
    profile.value = result.profile;
    selectedInterests.value = (result.profile.interests || []).map(
      (item) => item.name,
    );
    message.value = "Profile updated successfully.";
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const refreshPhotos = async () => {
  photos.value = await getMyPhotos();
};

const handleFileSelect = async (event) => {
  const files = Array.from(event.target.files || []);
  if (!files.length) return;
  await handlePhotoUpload(files);
  event.target.value = "";
};

const handlePhotoUpload = async (files) => {
  message.value = "";
  errorMessage.value = "";

  try {
    await uploadPhotos(files);
    await refreshPhotos();
    message.value = "Photos uploaded successfully.";
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const handleDrop = async (event) => {
  dragActive.value = false;
  const files = Array.from(event.dataTransfer.files || []);
  if (!files.length) return;
  await handlePhotoUpload(files);
};

const handleDeletePhoto = async (photoId) => {
  message.value = "";
  errorMessage.value = "";

  try {
    await deletePhoto(photoId);
    await refreshPhotos();
    message.value = "Photo deleted successfully.";
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const handleSetPrimary = async (photoId) => {
  message.value = "";
  errorMessage.value = "";

  try {
    await setPrimaryPhoto(photoId);
    await refreshPhotos();
    message.value = "Primary photo updated.";
  } catch (error) {
    errorMessage.value = error.message;
  }
};

const toggleInterest = (interestName) => {
  const normalized = interestName.trim().toLowerCase();

  if (selectedInterests.value.includes(normalized)) {
    selectedInterests.value = selectedInterests.value.filter(
      (item) => item !== normalized,
    );
  } else {
    selectedInterests.value.push(normalized);
  }
};

const addCustomInterest = () => {
  const normalized = newInterest.value.trim().toLowerCase();

  if (!normalized) return;

  if (!allInterests.value.includes(normalized)) {
    allInterests.value.push(normalized);
  }

  if (!selectedInterests.value.includes(normalized)) {
    selectedInterests.value.push(normalized);
  }

  newInterest.value = "";
};

onMounted(() => {
  loadProfile();
});
</script>

<template>
  <main class="profile-page">
    <aside class="sidebar">
      <nav>
        <RouterLink to="/dashboard">Browse</RouterLink>
        <RouterLink to="/me/profile">My Profile</RouterLink>
        <RouterLink to="/matches">Matches</RouterLink>
      </nav>
    </aside>

    <div class="content">
      <h2>My Profile</h2>

      <p v-if="message" class="success">{{ message }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="loading">Loading profile...</p>

      <div v-if="!loading" class="profile-card">
        <img
          class="profile-image"
          :src="imageUrl(profile.profile_picture)"
          alt="profile picture"
        />

        <div
          class="drop-zone"
          :class="{ active: dragActive }"
          @dragover.prevent="dragActive = true"
          @dragleave.prevent="dragActive = false"
          @drop.prevent="handleDrop"
        >
          <p>Drag and drop photos here</p>
          <p>or</p>
          <label for="photoUpload" class="upload-btn">Choose Photos</label>
          <input
            id="photoUpload"
            type="file"
            accept=".png,.jpg,.jpeg,.webp"
            multiple
            @change="handleFileSelect"
            hidden
          />
        </div>

        <div class="photo-gallery">
          <div class="photo-card" v-for="photo in photos" :key="photo.id">
            <img :src="imageUrl(photo.image_url)" alt="uploaded photo" />
            <p v-if="photo.is_primary" class="primary-badge">Primary</p>

            <div class="photo-actions">
              <button
                type="button"
                class="small-btn"
                @click="handleSetPrimary(photo.id)"
              >
                Set Primary
              </button>
              <button
                type="button"
                class="small-btn delete"
                @click="handleDeletePhoto(photo.id)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>

        <input
          v-model="profile.display_name"
          type="text"
          placeholder="Display name"
        />
        <input v-model="profile.age" type="number" placeholder="Age" />
        <textarea v-model="profile.bio" placeholder="Bio"></textarea>
        <input v-model="profile.location" type="text" placeholder="Location" />
        <input v-model="profile.gender" type="text" placeholder="Gender" />
        <input
          v-model="profile.looking_for"
          type="text"
          placeholder="Looking for"
        />

        <select v-model="profile.visibility">
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>

        <input
          v-model="profile.min_preferred_age"
          type="number"
          placeholder="Minimum preferred age"
        />
        <input
          v-model="profile.max_preferred_age"
          type="number"
          placeholder="Maximum preferred age"
        />
        <input
          v-model="profile.preferred_radius_km"
          type="number"
          placeholder="Preferred radius (km)"
        />

        <div class="interests-section">
          <h3>Choose Your Interests</h3>
          <p class="interest-note">Select at least 3 interests.</p>

          <div class="interest-list">
            <button
              v-for="interest in allInterests"
              :key="interest"
              type="button"
              class="interest-chip"
              :class="{ selected: selectedInterests.includes(interest) }"
              @click="toggleInterest(interest)"
            >
              {{ formatInterestName(interest) }}
            </button>
          </div>

          <div class="custom-interest-row">
            <input
              v-model="newInterest"
              type="text"
              placeholder="Add custom interest"
            />
            <button type="button" class="small-btn" @click="addCustomInterest">
              Add
            </button>
          </div>

          <p class="selected-count">Selected: {{ selectedInterests.length }}</p>
        </div>

        <button class="save-btn" @click="handleSave" type="button">
          Save Profile
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped>
.profile-page {
  display: grid;
  grid-template-columns: 0.6fr 4fr;
  min-height: 100vh;
}

.sidebar {
  padding: 2rem;
  background: var(--secondary-color);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar a {
  text-decoration: none;
  color: white;
  font-weight: 600;
}

.content {
  padding: 2rem;
}

h2 {
  text-align: center;
}

.profile-card {
  max-width: 700px;
  margin: 2rem auto;
  background: white;
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-image {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 20px;
  margin: 0 auto;
}

.drop-zone {
  border: 2px dashed #ccc;
  border-radius: 18px;
  padding: 1.5rem;
  text-align: center;
  background: #fafafa;
}

.drop-zone.active {
  border-color: var(--primary-color);
  background: #fff5f5;
}

.upload-btn {
  display: inline-block;
  padding: 0.7rem 1rem;
  background: var(--primary-color);
  color: white;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.photo-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 1rem;
}

.photo-card {
  background: #f8f8f8;
  border-radius: 16px;
  padding: 0.6rem;
  text-align: center;
}

.photo-card img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 12px;
}

.primary-badge {
  color: green;
  font-weight: 700;
  margin-top: 0.4rem;
}

.photo-actions {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 0.5rem;
}

.small-btn {
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 10px;
  background: var(--primary-color);
  color: white;
  cursor: pointer;
}

.small-btn.delete {
  background: #dc2626;
}

.profile-card input,
.profile-card textarea,
.profile-card select {
  padding: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 12px;
}

.profile-card textarea {
  min-height: 100px;
}

.interests-section {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.interests-section h3 {
  margin: 0;
}

.interest-note,
.selected-count {
  margin: 0;
  color: #4b5563;
}

.interest-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.interest-chip {
  border: 1px solid #d1d5db;
  background: #f9fafb;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  cursor: pointer;
}

.interest-chip.selected {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.custom-interest-row {
  display: flex;
  gap: 0.8rem;
}

.custom-interest-row input {
  flex: 1;
}

.save-btn {
  padding: 0.9rem;
  border: none;
  border-radius: 12px;
  background: var(--primary-color);
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.success {
  color: green;
  text-align: center;
}

.error {
  color: red;
  text-align: center;
}

@media (max-width: 900px) {
  .profile-page {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .sidebar nav {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }

  .custom-interest-row {
    flex-direction: column;
  }
}
</style>
