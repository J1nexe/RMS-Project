<template>
  <div class="classroom-container">
    <topNavbar />
    <div class="content-below-navbar">
      <div class="stats-container">
        <div class="stat-card">
          <h3>Total Students</h3>
          <div class="stat-number">{{ totalStudents }}</div>
          <div class="stat-trend">↑ 5% from last month</div>
        </div>
        <div class="stat-card">
          <h3>Active Courses</h3>
          <div class="stat-number">{{ uniqueCourses.length }}</div>
          <div class="stat-trend">Current Semester</div>
        </div>
        <div class="stat-card">
          <h3>Class Sections</h3>
          <div class="stat-number">{{ uniqueSections.length }}</div>
          <div class="stat-trend">Active Sections</div>
        </div>
      </div>

      <div class="search-section">
        <input type="text" v-model="searchQuery" placeholder="Search students..." class="search-input">
        <select v-model="filterCourse" class="filter-select">
          <option value="">All Courses</option>
          <option v-for="course in uniqueCourses" :key="course" :value="course">{{ course }}</option>
        </select>
      </div>

      <div class="students-grid">
        <div v-for="student in filteredStudents" :key="student.id" class="student-card">
          <div class="student-avatar">{{ getInitials(student.name) }}</div>
          <div class="student-info">
            <h3>{{ student.name }}</h3>
            <p class="course">{{ student.course }}</p>
            <p class="section">{{ student.yearAndSection }}</p>
          </div>          <div class="card-actions">
            <button @click="openIdModal(student.id)" class="view-details">View ID</button>
          </div>
        </div>
      </div>
    </div>
    <StudentIdModal 
      :show="showIdModal"
      :student-id="selectedStudentId"
      @close="closeIdModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import topNavbar from '../components/topNavbar.vue';
import StudentIdModal from '../components/id.vue';

const students = ref([]);
const searchQuery = ref('');
const filterCourse = ref('');
const STUDENT_RECORDS_API_URL = 'http://localhost:8000/api/student-records/';

const totalStudents = computed(() => students.value.length);

const uniqueCourses = computed(() => {
  const courses = new Set(students.value.map(s => s.course));
  return Array.from(courses);
});

const uniqueSections = computed(() => {
  const sections = new Set(students.value.map(s => s.yearAndSection));
  return Array.from(sections);
});

const filteredStudents = computed(() => {
  return students.value.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         student.course.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCourse = !filterCourse.value || student.course === filterCourse.value;
    return matchesSearch && matchesCourse;
  });
});

function getInitials(name) {
  return name.split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

async function fetchStudents() {
  try {
    const response = await axios.get(STUDENT_RECORDS_API_URL);
    students.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    console.error('Error fetching students:', error);
  }
}

onMounted(() => {
  fetchStudents();
});

const showIdModal = ref(false);
const selectedStudentId = ref(null);

function openIdModal(studentId) {
  selectedStudentId.value = studentId;
  showIdModal.value = true;
}

function closeIdModal() {
  showIdModal.value = false;
  selectedStudentId.value = null;
}
</script>

<style scoped>
.classroom-container {
  min-height: 100vh;
  background: #f5f7fa;
  font-family: 'Poppins', sans-serif;
}

.content-below-navbar {
  padding: 90px 40px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 12px 0;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.stat-trend {
  color: #4caf50;
  font-size: 0.85rem;
}

.search-section {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
}

.search-input, .filter-select {
  padding: 12px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.search-input:focus, .filter-select:focus {
  border-color: #4A4AFF;
  outline: none;
  box-shadow: 0 0 0 3px rgba(74, 74, 255, 0.1);
}

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.student-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.student-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.student-avatar {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #4A4AFF, #8C4AFF);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 16px;
}

.student-info h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 1.2rem;
}

.course {
  color: #666;
  margin: 0 0 4px 0;
  font-size: 0.9rem;
}

.section {
  color: #888;
  margin: 0 0 16px 0;
  font-size: 0.85rem;
}

.view-details {
  display: inline-block;
  padding: 8px 20px;
  background: #4A4AFF;
  color: white;
  text-decoration: none;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.view-details:hover {
  background: #3939CC;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .content-below-navbar {
    padding: 80px 20px 20px;
  }

  .search-section {
    flex-direction: column;
  }

  .search-input {
    max-width: none;
  }
}
</style>
