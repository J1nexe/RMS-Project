<template>
  <div class="data-page-wrapper">
    <TopNavbar />
    <main class="content-below-navbar">
      <div class="page-content">
        <h1>Student Management</h1>

        <!-- API Error Alert -->
        <div v-if="apiError" class="api-error-alert">
          <div>
            <strong>Connection Error:</strong> {{ apiError }}
          </div>
          <button @click="fetchStudents" class="retry-btn">Retry</button>
        </div>

        <div class="controls">
          <input type="text" v-model="searchQuery" placeholder="Search students..." class="search-input">
          <button @click="openAddStudentModal" class="add-student-btn">Add Student</button>
        </div>

        <div class="table-scroll-wrapper">
          <table class="students-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Student ID</th>
                <th>Name</th>
                <th>Course</th>
                <th>Year & Section</th>
                <th>Contact Number</th>
                <th>Address</th>
                <th>Date of Birth</th>
                <th>Gender</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isLoading">
                <td colspan="9" class="no-data">
                  <div class="loading-spinner"></div>
                  Loading students...
                </td>
              </tr>
              <tr v-else-if="initialLoadError">
                <td colspan="9" class="no-data error-message">
                  {{ apiError || 'Could not load student data. Please try again later.' }}
                </td>
              </tr>
              <tr v-else-if="paginatedStudents.length === 0 && students.length > 0">
                <td colspan="9" class="no-data">No students match your search.</td>
              </tr>
              <tr v-else-if="paginatedStudents.length === 0">
                <td colspan="9" class="no-data">No students found. Add one!</td>
              </tr>
              <tr v-for="student in paginatedStudents" :key="student.id" class="student-row">
                <td>{{ student.id }}</td>
                <td>{{ student.studentID }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.course }}</td>
                <td>{{ student.yearAndSection }}</td>
                <td>{{ student.contactNumber }}</td>
                <td>{{ student.address }}</td>
                <td>{{ formatDate(student.dateOfBirth) }}</td>
                <td>{{ student.gender }}</td>
                <td class="actions">
                  <button class="action-btn view-id-btn" @click="openIdModal(student.id)">
                    View ID
                  </button>
                  <button @click="editStudent(student)" class="action-btn edit-btn">Edit</button>
                  <button @click="deleteStudent(student.id)" class="action-btn delete-btn">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination" v-if="totalPages > 1 && !isLoading && !initialLoadError">
          <button @click="prevPage" :disabled="currentPage === 1" class="pagination-btn">Previous</button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-btn">Next</button>
        </div>

        <!-- Add/Edit Student Modal -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <span class="close-btn" @click="closeModal">&times;</span>
            <h2>{{ isEditing ? 'Edit Student' : 'Add Student' }}</h2>
            
            <form @submit.prevent="saveStudent">
              <div class="form-group">
                <label for="name">Full Name:</label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="currentStudent.name" 
                  placeholder="Enter student's full name"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="course">Course/Program:</label>
                <input 
                  type="text" 
                  id="course" 
                  v-model="currentStudent.course" 
                  placeholder="e.g. Computer Science"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="yearAndSection">Year & Section:</label>
                <input 
                  type="text" 
                  id="yearAndSection" 
                  v-model="currentStudent.yearAndSection" 
                  placeholder="e.g. 3-A"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="contactNumber">Contact Number:</label>
                <input 
                  type="text" 
                  id="contactNumber" 
                  v-model="currentStudent.contactNumber" 
                  placeholder="Enter phone number"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="address">Address:</label>
                <input 
                  type="text" 
                  id="address" 
                  v-model="currentStudent.address" 
                  placeholder="Enter complete address"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="dateOfBirth">Date of Birth:</label>
                <input 
                  type="date" 
                  id="dateOfBirth" 
                  v-model="currentStudent.dateOfBirth"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="gender">Gender:</label>
                <select 
                  id="gender" 
                  v-model="currentStudent.gender" 
                  required
                >
                  <option value="" disabled>Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              
              <div v-if="modalError" class="modal-error-message">
                {{ modalError }}
              </div>
              
              <button type="submit" class="save-btn" :disabled="isSaving">
                {{ isSaving ? 'Saving...' : (isEditing ? 'Save Changes' : 'Add Student') }}
              </button>
            </form>
          </div>
        </div>

        <!-- Student ID Modal -->
        <StudentIdModal 
          :show="showIdModal"
          :student-id="selectedStudentId"
          @close="closeIdModal"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';
import TopNavbar from '../components/topNavbar.vue';
import StudentIdModal from '../components/id.vue';

// Enable debug mode for development
const DEBUG_MODE = true;

// Ensure trailing slash is consistent in the API URL
const STUDENT_RECORDS_API_URL = 'http://localhost:8000/api/student-records/';

const students = ref([]);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;

const showModal = ref(false);
const isEditing = ref(false);
const currentStudent = ref({
  id: null,
  name: '',
  course: '',
  yearAndSection: '',
  contactNumber: '',
  address: '',
  dateOfBirth: '',
  gender: ''
});

const isLoading = ref(false);
const isSaving = ref(false);
const initialLoadError = ref(false);
const modalError = ref('');
const apiError = ref('');

const showIdModal = ref(false);
const selectedStudentId = ref(null);

// Add date formatting function
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Configure axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.timeout = 10000; // 10 seconds timeout

// Add error handling for API connection
async function checkApiConnection() {
  try {
    if (DEBUG_MODE) console.log('Checking API connection...');
    // Try a GET request instead of HEAD as some APIs may not support HEAD
    const response = await axios.get(STUDENT_RECORDS_API_URL);
    if (DEBUG_MODE) console.log('API connection successful:', response.status);
    return true;
  } catch (error) {
    console.error('API connection error:', error);
    if (error.response) {
      apiError.value = `Server error: ${error.response.status} - ${error.response.statusText}`;
    } else if (error.request) {
      apiError.value = 'Cannot connect to the server. Please check if the backend service is running.';
    } else {
      apiError.value = 'Error preparing the request. Please try again.';
    }
    return false;
  }
}

async function fetchStudents() {
  isLoading.value = true;
  initialLoadError.value = false;
  apiError.value = '';

  if (DEBUG_MODE) console.log('Fetching students...');

  try {
    // First check API connection
    const isConnected = await checkApiConnection();
    if (!isConnected) {
      initialLoadError.value = true;
      students.value = []; // Ensure it's an empty array
      return;
    }

    const response = await axios.get(STUDENT_RECORDS_API_URL);
    if (DEBUG_MODE) console.log('API Response:', response.data); // Debug: log the response
    
    // Handle different response formats
    if (Array.isArray(response.data)) {
      students.value = response.data;
      if (DEBUG_MODE) console.log('Loaded students (array):', students.value.length);
    } else if (response.data.results && Array.isArray(response.data.results)) {
      // Handle DRF paginated response
      students.value = response.data.results;
      if (DEBUG_MODE) console.log('Loaded students (paginated):', students.value.length);
    } else if (typeof response.data === 'object') {
      // If it's an object with student records
      const studentArray = Object.values(response.data);
      students.value = studentArray;
      if (DEBUG_MODE) console.log('Loaded students (object):', students.value.length);
    } else {
      students.value = [];
      console.error('Unexpected API response format:', response.data);
    }
  } catch (error) {
    console.error('Error fetching students:', error);
    students.value = []; // Ensure it's an empty array
    initialLoadError.value = true;
    if (error.response) {
      apiError.value = `Server error: ${error.response.status} - ${error.response.statusText}`;
    } else if (error.request) {
      apiError.value = 'No response from server. Please check your connection.';
    } else {
      apiError.value = 'Error preparing the request. Please try again.';
    }
  } finally {
    isLoading.value = false;
  }
}

// Fetch students when component mounts
onMounted(() => {
  if (DEBUG_MODE) console.log('Component mounted, fetching students...');
  fetchStudents();
});

const filteredStudents = computed(() => {
  // Ensure students.value is an array
  const studentsArray = Array.isArray(students.value) ? students.value : [];
  
  if (!searchQuery.value) {
    return studentsArray;
  }
  
  const query = searchQuery.value.toLowerCase();
  return studentsArray.filter(student => {
    if (!student) return false;
    return (
      (student.name && student.name.toLowerCase().includes(query)) ||
      (student.course && student.course.toLowerCase().includes(query)) ||
      (student.yearAndSection && student.yearAndSection.toLowerCase().includes(query))
    );
  });
});

const totalPages = computed(() => {
  return Math.ceil((filteredStudents.value?.length || 0) / itemsPerPage);
});

const paginatedStudents = computed(() => {
  // Ensure filteredStudents.value is an array
  const filtered = Array.isArray(filteredStudents.value) ? filteredStudents.value : [];
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filtered.slice(start, end);
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function openAddStudentModal() {
  isEditing.value = false;
  currentStudent.value = { 
    id: null, 
    name: '', 
    course: '', 
    yearAndSection: '', 
    contactNumber: '', 
    address: '', 
    dateOfBirth: '', 
    gender: '' 
  };
  modalError.value = '';
  showModal.value = true;
}

function editStudent(student) {
  isEditing.value = true;
  currentStudent.value = { ...student };
  modalError.value = '';
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  currentStudent.value = { 
    id: null, 
    name: '', 
    course: '', 
    yearAndSection: '', 
    contactNumber: '', 
    address: '', 
    dateOfBirth: '', 
    gender: '' 
  }; // Reset form without email field
  modalError.value = '';
}

async function saveStudent() {
  isSaving.value = true;
  modalError.value = '';
  try {
    let response;
    const studentData = {
      name: currentStudent.value.name,
      course: currentStudent.value.course,
      yearAndSection: currentStudent.value.yearAndSection,
      contactNumber: currentStudent.value.contactNumber,
      address: currentStudent.value.address,
      dateOfBirth: currentStudent.value.dateOfBirth,
      gender: currentStudent.value.gender,
    };

    if (isEditing.value) {
      response = await axios.put(`${STUDENT_RECORDS_API_URL}${currentStudent.value.id}/`, studentData);
      const index = students.value.findIndex(s => s.id === currentStudent.value.id);
      if (index !== -1) {
        students.value[index] = response.data;
      }
    } else {
      response = await axios.post(STUDENT_RECORDS_API_URL, studentData);
      students.value.push(response.data);
    }
    closeModal();
    // Refresh the student list to ensure we have the latest data
    fetchStudents();
  } catch (error) {
    console.error('Error saving student:', error);
    if (error.response && error.response.data) {
      if (typeof error.response.data === 'object') {
        modalError.value = Object.values(error.response.data).flat().join(' ');
      } else {
        modalError.value = error.response.data;
      }
    } else if (error.request) {
      modalError.value = 'No response from server. Please check your connection.';
    } else {
      modalError.value = 'An unexpected error occurred. Please try again.';
    }
  } finally {
    isSaving.value = false;
  }
}

async function deleteStudent(studentId) {
  if (confirm('Are you sure you want to delete this student?')) {
    try {
      if (DEBUG_MODE) console.log(`Deleting student with ID: ${studentId}`);
      
      await axios.delete(`${STUDENT_RECORDS_API_URL}${studentId}/`);
      
      // Update the local students array
      students.value = students.value.filter(s => s.id !== studentId);
      
      // Adjust pagination if needed
      if (paginatedStudents.value.length === 0 && currentPage.value > 1) {
        currentPage.value--;
      }
      
      // Refresh the student list to ensure consistency with the database
      fetchStudents();
      
    } catch (error) {
      console.error('Error deleting student:', error);
      let errorMessage = 'Failed to delete student. ';
      
      if (error.response) {
        const status = error.response.status;
        if (status === 404) {
          // If the student was not found, it might have been already deleted
          errorMessage = 'Student not found. It may have been already deleted.';
          // Remove from local array anyway
          students.value = students.value.filter(s => s.id !== studentId);
        } else {
          errorMessage += `Server error: ${status}`;
          if (error.response.data && error.response.data.error) {
            errorMessage += ` - ${error.response.data.error}`;
          }
        }
      } else if (error.request) {
        errorMessage += 'No response from server. Please check your connection.';
      } else {
        errorMessage += 'Please try again.';
      }
      
      alert(errorMessage);
    }
  }
}

function openIdModal(studentId) {
  selectedStudentId.value = studentId;
  showIdModal.value = true;
}

function closeIdModal() {
  showIdModal.value = false;
  selectedStudentId.value = null;
}

watch(searchQuery, () => {
  currentPage.value = 1;
});

// If students array changes (e.g. after add/delete), ensure currentPage is valid
watch(students, () => {
    if(currentPage.value > totalPages.value && totalPages.value > 0) {
        currentPage.value = totalPages.value;
    } else if (totalPages.value === 0) {
        currentPage.value = 1;
    }
}, { deep: true });

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* CSS Variables for Theme */
:root {
  --primary-color: #4A4AFF;
  --primary-hover-color: #3939CC;
  --accent-color: #00C853;
  --accent-hover-color: #00A844;
  --background-color: #F0F2F5;
  --content-bg-color: #FFFFFF;
  --text-primary-color: #000000;
  --text-secondary-color: #333333;
  --border-color: #CCCCCC;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --danger-hover-color: #c82333;
  --warning-color: #ffc107;
  --button-border-radius: 8px;
  --card-border-radius: 12px;
  --box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  --box-shadow-light: 0 4px 8px rgba(0, 0, 0, 0.05);
}

/* Overall page structure */
.data-page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background-color: var(--background-color);
  font-family: 'Poppins', sans-serif;
  color: #333; /* Dark gray text color for better visibility */
}

.content-below-navbar {
  padding: 20px; /* Reduced top padding as navbar might provide its own */
  flex: 1;
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: flex-start;
  padding-top: 80px; /* Assuming navbar height is around 60-80px */
}

/* Main content area */
.page-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background-color: var(--content-bg-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--box-shadow);
  display: flex;
  flex-direction: column;
  padding: 30px;
  box-sizing: border-box;
  min-height: calc(100vh - 120px); /* Adjust based on navbar and padding */
}

h1 {
  text-align: center;
  color: var(--text-primary-color);
  margin-bottom: 30px;
  font-size: 2.2rem;
  font-weight: 600;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
  width: 100%;
}

.search-input {
  padding: 12px 18px;
  border: 1px solid var(--border-color);
  border-radius: var(--button-border-radius);
  width: 100%;
  max-width: 350px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  color: var(--text-primary-color);
  background-color: #FFFFFF;
}

.search-input::placeholder {
  color: var(--text-secondary-color);
  opacity: 0.8;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 74, 255, 0.15);
}

.add-student-btn,
.save-btn {
  padding: 12px 25px;
  background: linear-gradient(135deg, #4A4AFF 0%, #8C4AFF 100%);
  color: #FFFFFF;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(74, 74, 255, 0.2);
  display: inline-block;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.add-student-btn:hover {
  background-color: #3939CC;  /* Darker blue on hover */
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Table container */
.table-scroll-wrapper {
  width: 100%;
  margin: 0;
  padding: 0;
}

.students-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.students-table th,
.students-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #edf2f7;
  border-right: 1px solid #edf2f7;
  color: #333;
}

.students-table th {
  background: linear-gradient(135deg, #4A4AFF 0%, #8C4AFF 100%);
  color: white;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.student-row:nth-child(even) {
  background-color: #F8F9FA;
}

.student-row:hover {
  background-color: #f5f5f5;
}

.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  margin: 0 4px;
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.view-id-btn {
  background: linear-gradient(135deg, #4A4AFF, #8C4AFF);
}

.view-id-btn:hover {
  background: #3939CC;
}

.edit-btn {
  background-color: #28a745;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn {
  background-color: #dc3545;
}

.delete-btn:hover {
  background-color: var(--danger-hover-color);
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  color: var(--danger-color);
  font-weight: 500;
}

/* Pagination */
.pagination {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  color: #333;
}

.pagination-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Modal Styles - Improved */
.modal {
  position: fixed;
  z-index: 1050;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: rgba(0, 0, 0, 0.75); /* Darker overlay */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background-color: #ffffff; /* Solid white background */
  padding: 30px 35px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  color: #333;
  border: 1px solid #e0e0e0;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  color: #666;
  transition: color 0.2s;
  line-height: 1;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f8f9fa;
}

.close-btn:hover {
  color: #333;
  background-color: #e9ecef;
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 25px;
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.form-group {
  margin-bottom: 20px;
  background-color: #ffffff;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 0.95rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  color: #333;
  background-color: #ffffff;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #4A4AFF;
  outline: none;
  box-shadow: 0 0 0 3px rgba(74, 74, 255, 0.15);
}

.form-group input::placeholder {
  color: #999;
}

.save-btn {
  background-color: #4A4AFF;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  margin-top: 20px;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.save-btn:hover:not(:disabled) {
  background-color: #3939CC;
  transform: translateY(-1px);
}

.save-btn:disabled {
  background-color: #B0BEC5;
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

.modal-error-message {
  color: #dc3545;
  margin-top: 15px;
  text-align: center;
  padding: 10px;
  background-color: #fff5f5;
  border-radius: 6px;
  font-size: 0.9rem;
}

/* API error alert styles */
.api-error-alert {
  background-color: #fff3cd;
  color: #856404;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.retry-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.loading-spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive styles */
@media (max-width: 1024px) {
  .content-below-navbar {
    padding: 80px 15px 15px;
  }
  
  .page-content {
    padding: 20px;
  }

  .students-table th,
  .students-table td {
    padding: 12px 10px;
    font-size: 0.9rem; /* Slightly smaller font for smaller screens */
  }
}

@media (max-width: 768px) {
  .content-below-navbar {
    padding: 70px 0 0; /* No side padding, let page-content handle it */
  }

  .page-content {
    padding: 20px; /* Uniform padding */
    border-radius: 0; /* Full width on mobile */
    min-height: calc(100vh - 70px);
    box-shadow: none; /* Remove shadow on mobile for edge-to-edge */
  }

  h1 {
    font-size: 1.8rem;
  }

  .controls {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .search-input,
  .add-student-btn {
    width: 100%;
    max-width: none;
  }
  
  .modal-content {
    padding: 20px 25px;
    width: 100%;
    max-width: calc(100% - 30px); /* Some margin from screen edges */
    margin: auto;
    max-height: 85vh;
  }

  .modal h2 {
    font-size: 1.6rem;
  }

  .api-error-alert {
    flex-direction: column;
    align-items: stretch;
    padding: 15px;
  }

  .retry-btn {
    width: 100%;
    padding: 10px;
  }

  .action-btn {
    padding: 6px 10px; /* Smaller buttons on mobile */
    font-size: 0.8rem;
  }

  .actions {
    gap: 6px;
  }
}
</style>