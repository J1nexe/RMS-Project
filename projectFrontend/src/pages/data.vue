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
                <td>{{ student.name }}</td>
                <td>{{ student.course }}</td>
                <td>{{ student.yearAndSection }}</td>
                <td>{{ student.contactNumber }}</td>
                <td>{{ student.address }}</td>
                <td>{{ formatDate(student.dateOfBirth) }}</td>
                <td>{{ student.gender }}</td>
                <td class="actions">
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
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';
import TopNavbar from '../components/topNavbar.vue'; // Adjusted path

// Enable debug mode for development
const DEBUG_MODE = true;

// Ensure trailing slash is consistent in the API URL
const STUDENT_RECORDS_API_URL = 'http://localhost:8000/api/student-records/';

const students = ref([]);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;

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

/* Overall page structure */
.data-page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background-color: #eef1f5;
  position: relative;
}

.content-below-navbar {
  padding: 80px 20px 20px;
  flex: 1;
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: flex-start;
}

/* Main content area */
.page-content {
  font-family: 'Poppins', sans-serif;
  width: 100%;
  max-width: 1400px; /* Set a max-width for larger screens */
  margin: 0 auto;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  padding: 25px;
  box-sizing: border-box;
  min-height: calc(100vh - 100px); /* Adjust based on navbar height */
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 2rem;
  font-weight: 600;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
}

.search-input {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  width: 100%;
  max-width: 320px;
  font-size: 1rem;
}

.search-input::placeholder {
  color: #888;
  opacity: 1;
}

.add-student-btn {
  padding: 12px 22px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.add-student-btn:hover {
  background-color: #218838;
}

/* Table container */
.table-scroll-wrapper {
  width: 100%;
  overflow-x: auto;
  margin: 0;
  padding: 0;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  background-color: #fff;
}

.students-table th,
.students-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

/* Column widths */
.students-table th:nth-child(1), /* ID */
.students-table td:nth-child(1) {
  width: 5%;
  min-width: 50px;
}

.students-table th:nth-child(2), /* Name */
.students-table td:nth-child(2) {
  width: 15%;
  min-width: 120px;
}

.students-table th:nth-child(3), /* Course */
.students-table td:nth-child(3) {
  width: 15%;
  min-width: 120px;
}

.students-table th:nth-child(4), /* Year & Section */
.students-table td:nth-child(4) {
  width: 10%;
  min-width: 100px;
}

.students-table th:nth-child(5), /* Contact Number */
.students-table td:nth-child(5) {
  width: 12%;
  min-width: 120px;
}

.students-table th:nth-child(6), /* Address */
.students-table td:nth-child(6) {
  width: 20%;
  min-width: 150px;
}

.students-table th:nth-child(7), /* Date of Birth */
.students-table td:nth-child(7) {
  width: 12%;
  min-width: 120px;
}

.students-table th:nth-child(8), /* Gender */
.students-table td:nth-child(8) {
  width: 8%;
  min-width: 80px;
}

.students-table th:nth-child(9), /* Actions */
.students-table td:nth-child(9) {
  width: 10%;
  min-width: 100px;
}

.students-table td {
  color: #333;
  font-size: 0.95rem;
}

.students-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  color: #495057;
  position: sticky;
  top: 0;
  z-index: 10;
}

.student-row:hover {
  background-color: #e9ecef !important;
  transition: background-color 0.2s ease;
}

.actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.edit-btn {
  background-color: #ffc107;
  color: #212529;
}

.edit-btn:hover {
  background-color: #e0a800;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.no-data {
  text-align: center;
  padding: 30px 20px;
  color: #6c757d;
  font-style: italic;
  font-size: 1.1rem;
}

.error-message {
  color: #dc3545;
  font-weight: 500;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.pagination-btn:disabled {
  background-color: #ced4da;
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
  overflow: auto;
  background-color: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  width: 90%;
  max-width: 550px;
  position: relative;
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
}

.close-btn:hover {
  color: #333;
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 25px;
  text-align: center;
  color: #2c3e50;
  font-size: 1.8rem;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.form-group {
  margin-bottom: 22px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 0.95rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: #fff;
  color: #333;
  height: 45px; /* Fixed height for consistency */
  line-height: normal;
  -webkit-appearance: none; /* Remove default styles */
  -moz-appearance: none;
  appearance: none;
}

/* Special styling for date input */
.form-group input[type="date"] {
  padding-right: 15px; /* Space for the calendar icon */
}

/* Custom select arrow */
.form-group select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23495057' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
  padding-right: 40px; /* Space for the arrow */
}

.form-group input:focus,
.form-group select:focus {
  border-color: #80bdff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
}

.form-group input::placeholder {
  color: #6c757d;
  opacity: 0.8;
}

/* Remove default select arrow in IE */
.form-group select::-ms-expand {
  display: none;
}

/* Style for select options */
.form-group select option {
  padding: 12px;
  font-size: 1rem;
  color: #333;
  background-color: #fff;
}

.save-btn {
  width: 100%;
  padding: 14px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.05rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 10px;
  height: 48px;
}

.save-btn:hover {
  background-color: #218838;
}

.save-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

.modal-error-message {
  color: #dc3545;
  font-size: 0.9em;
  margin: 15px 0;
  text-align: center;
  padding: 10px;
  background-color: rgba(220, 53, 69, 0.1);
  border-radius: 4px;
  font-weight: 500;
}

/* API error alert styles */
.api-error-alert {
  background-color: #fff3cd;
  color: #856404;
  padding: 15px;
  margin-bottom: 25px;
  border: 1px solid #ffeeba;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.retry-btn {
  background-color: #856404;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.retry-btn:hover {
  background-color: #6d5204;
}

.loading-spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  margin-right: 12px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive styles */
@media (max-width: 1024px) {
  .content-below-navbar {
    padding: 80px 10px 20px;
  }
  
  .table-scroll-wrapper {
    margin: 0;
    padding: 0;
    width: 100%;
    overflow-x: auto;
  }

  .students-table {
    min-width: 800px; /* Ensure table doesn't shrink too much */
  }

  .students-table th,
  .students-table td {
    padding: 12px 10px;
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .content-below-navbar {
    padding: 70px 0 0;
  }

  .page-content {
    padding: 15px;
    border-radius: 0;
    min-height: calc(100vh - 70px);
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
    padding: 20px;
    width: 95%;
  }

  .api-error-alert {
    flex-direction: column;
    align-items: stretch;
  }

  .retry-btn {
    width: 100%;
  }
}
</style>