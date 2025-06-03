<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="id-container" @click.stop>
      <button class="close-button" @click="closeModal">&times;</button>
      <div class="id-card" :class="{ 'is-flipped': isFlipped }" @click="flipCard">
        <!-- Front of ID -->
        <div class="id-side front">
          <div class="header">
            <h2>Student Identification Card</h2>
          </div>
          <div class="student-avatar">{{ getInitials(studentData.name) }}</div>          <div class="student-info">
            <h3>{{ studentData.name }}</h3>
            <p class="course">{{ studentData.course }}</p>
            <p class="section">{{ studentData.yearAndSection }}</p>
          </div>
          <div class="flip-hint">Click to view back</div>
        </div>

        <!-- Back of ID -->
        <div class="id-side back">
          <div class="header">
            <h2>Contact Information</h2>
          </div>
          <div class="contact-info">
            <div class="info-row">
              <label>Contact Number:</label>
              <p>{{ studentData.contactNumber }}</p>
            </div>
            <div class="info-row">              <label>Address:</label>
              <p>{{ studentData.address }}</p>
            </div>
          </div>
          <div class="academic-years">
            <h3>Academic Years</h3>
            <div v-for="(year, index) in academicYears" :key="index" class="year-entry">
              <span class="year-label">Year {{ index + 1 }}:</span>
              <span class="year-value">{{ year }}</span>
            </div>
          </div>
          <div class="flip-hint">Click to view front</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import axios from 'axios';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  studentId: {
    type: [String, Number],
    default: ''
  }
});

const emit = defineEmits(['close']);

const isFlipped = ref(false);
const studentData = ref({
  name: '',
  course: '',
  yearAndSection: '',
  contactNumber: '',
  address: '',
});

const STUDENT_RECORDS_API_URL = 'http://localhost:8000/api/student-records/';

const academicYears = computed(() => {
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const startYear = currentDate.getMonth() >= 5 ? currentYear : currentYear - 1;
  const years = [];
  for (let i = 0; i < 4; i++) {
    years.push(`${startYear + i}-${startYear + i + 1}`);
  }
  return years;
});

function getInitials(name) {
  return name.split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

function flipCard() {
  isFlipped.value = !isFlipped.value;
}

function closeModal() {
  isFlipped.value = false;
  emit('close');
}

async function fetchStudentData() {
  try {
    if (props.studentId) {
      const response = await axios.get(`${STUDENT_RECORDS_API_URL}${props.studentId}/`);
      studentData.value = response.data;
    }
  } catch (error) {
    console.error('Error fetching student data:', error);
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    fetchStudentData();
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.close-button {
  position: absolute;
  top: -40px;
  right: 0;
  background: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.id-container {
  position: relative;
  padding: 20px;
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: 'Poppins', sans-serif;
}

.id-card {
  width: 350px;
  height: 550px;
  position: relative;
  perspective: 1000px;
  cursor: pointer;
}

.id-side {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  transition: transform 0.6s;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.id-card.is-flipped .front {
  transform: rotateY(180deg);
}

.id-card.is-flipped .back {
  transform: rotateY(0);
}

.front {
  transform: rotateY(0);
}

.back {
  transform: rotateY(-180deg);
}

.header {
  text-align: center;
  margin-bottom: 24px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 16px;
}

.header h2 {
  color: #333;
  font-size: 1.2rem;
  margin: 0;
}

.student-avatar {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #4A4AFF, #8C4AFF);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0 auto 24px;
}

.student-info {
  text-align: center;
  margin-bottom: 24px;
}

.student-info h3 {
  margin: 0 0 8px;
  color: #333;
  font-size: 1.4rem;
}

.course {
  color: #666;
  margin: 0 0 4px;
  font-size: 1.1rem;
}

.section {
  color: #888;
  margin: 0;
  font-size: 1rem;
}

.academic-years {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e0e0e0;
}

.academic-years h3 {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 16px;
  text-align: center;
}

.year-entry {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.year-label {
  color: #666;
  font-weight: 600;
}

.year-value {
  color: #333;
}

.contact-info {
  margin-top: 24px;
}

.info-row {
  margin-bottom: 16px;
}

.info-row label {
  display: block;
  color: #666;
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

.info-row p {
  color: #333;
  margin: 0;
  font-size: 1rem;
}

.flip-hint {
  text-align: center;
  color: #888;
  font-size: 0.8rem;
  margin-top: auto;
  padding-top: 16px;
}

@media (max-width: 768px) {
  .id-card {
    width: 300px;
    height: 480px;
  }

  .student-avatar {
    width: 100px;
    height: 100px;
    font-size: 2rem;
  }
}
</style>