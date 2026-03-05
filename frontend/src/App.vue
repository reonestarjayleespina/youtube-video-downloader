<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
    <!-- Background elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute top-1/2 right-0 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-5xl sm:text-6xl font-bold mb-4">
          <span class="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            YouTube Downloader
          </span>
        </h1>
        <p class="text-gray-300 text-lg sm:text-xl max-w-2xl mx-auto">
          Download high-quality videos with your preferred resolution. Select your desired quality and let us handle the rest.
        </p>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left: URL Input & Video Info -->
        <div class="lg:col-span-2 space-y-6">
          <!-- URL Input Card -->
          <div class="glass p-8">
            <label class="block text-sm font-semibold text-gray-200 mb-3">YouTube URL</label>
            <div class="flex flex-col sm:flex-row gap-3">
              <input
                v-model="youtubeUrl"
                type="text"
                placeholder="https://www.youtube.com/watch?v=..."
                @keyup.enter="fetchFormats"
                class="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
              <button
                @click="fetchFormats"
                :disabled="!youtubeUrl || loading"
                class="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:from-gray-600 disabled:to-gray-600 text-white font-semibold rounded-lg transition-all duration-200 whitespace-nowrap"
              >
                <span v-if="!loading">Check</span>
                <span v-else class="flex items-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading...
                </span>
              </button>
            </div>
            <p v-if="error" class="mt-3 text-red-400 text-sm flex items-start gap-2">
              <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              {{ error }}
            </p>
          </div>

          <!-- Video Preview -->
          <div v-if="videoInfo && !loading" class="glass p-8 animate-fadeInScale">
            <div class="flex flex-col sm:flex-row gap-6">
              <!-- Thumbnail -->
              <div class="flex-shrink-0">
                <img
                  v-if="videoInfo.thumbnail"
                  :src="videoInfo.thumbnail"
                  :alt="videoInfo.title"
                  class="w-full sm:w-48 h-auto rounded-lg shadow-xl object-cover"
                />
              </div>
              <!-- Video Details -->
              <div class="flex-1">
                <h2 class="text-2xl font-bold text-white mb-2">{{ videoInfo.title }}</h2>
                <div class="space-y-2 text-gray-300">
                  <p>
                    <span class="text-gray-400">Duration:</span>
                    {{ formatDuration(videoInfo.duration) }}
                  </p>
                  <p>
                    <span class="text-gray-400">Available Formats:</span>
                    {{ videoInfo.formats.length }}
                  </p>
                  <p v-if="selectedFormat" class="text-blue-400">
                    <span class="text-gray-400">Selected:</span>
                    {{ selectedFormat.resolution }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Format Selection Grid -->
          <div v-if="videoInfo && videoInfo.formats.length > 0 && !loading" class="space-y-4 animate-fadeInScale">
            <h3 class="text-xl font-bold text-white">Select Resolution</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <button
                v-for="format in videoInfo.formats"
                :key="format.format_id"
                @click="selectedFormat = format"
                :class="[
                  'glass p-4 text-center rounded-lg transition-all duration-200 group hover:border-blue-400/50 hover:shadow-blue-500/20 hover:shadow-lg',
                  selectedFormat?.format_id === format.format_id
                    ? 'border-blue-400 shadow-blue-500/40 shadow-lg ring-2 ring-blue-500/20'
                    : 'border-white/20'
                ]"
              >
                <div class="text-lg font-bold text-white group-hover:text-blue-300 transition-colors">
                  {{ format.resolution }}
                </div>
                <div class="text-xs text-gray-400 mt-1">
                  {{ format.ext.toUpperCase() }}
                </div>
                <div v-if="format.filesize_mb > 0" class="text-xs text-gray-400 mt-1">
                  {{ (format.filesize_mb).toFixed(1) }} MB
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Right: Download & History Sidebar -->
        <div class="space-y-6">
          <!-- Download Card -->
          <div class="glass p-8 sticky top-6">
            <h3 class="text-xl font-bold text-white mb-4">Ready to Download?</h3>
            <button
              v-if="selectedFormat && videoInfo"
              @click="downloadVideo"
              :disabled="downloading"
              class="w-full px-6 py-4 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 disabled:from-gray-600 disabled:to-gray-600 text-white font-bold rounded-lg transition-all duration-200 flex items-center justify-center gap-2"
            >
              <svg v-if="!downloading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
              </svg>
              <span v-if="!downloading">Download Now</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Downloading...
              </span>
            </button>
            <button
              v-else
              disabled
              class="w-full px-6 py-4 bg-gray-600 text-gray-300 font-bold rounded-lg cursor-not-allowed"
            >
              Select a resolution first
            </button>

            <!-- Progress Bar -->
            <div v-if="downloading" class="mt-6">
              <div class="flex justify-between text-sm text-gray-300 mb-2">
                <span>Download Progress</span>
                <span>{{ downloadProgress }}%</span>
              </div>
              <div class="w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
                <div
                  class="bg-gradient-to-r from-green-400 to-emerald-500 h-full transition-all duration-300"
                  :style="{ width: downloadProgress + '%' }"
                ></div>
              </div>
            </div>

            <!-- Download Success -->
            <div v-if="downloadSuccess" class="mt-6 p-4 bg-green-500/20 border border-green-500/50 rounded-lg animate-fadeInScale">
              <p class="text-green-300 text-sm font-semibold flex items-center gap-2">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                Download complete!
              </p>
              <p class="text-green-200 text-xs mt-1">{{ downloadSuccess }}</p>
            </div>
          </div>

          <!-- Download History -->
          <div v-if="downloadHistory.length > 0" class="glass p-8">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-white">History</h3>
              <button
                @click="clearHistory"
                class="text-xs px-2 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded transition-colors"
              >
                Clear
              </button>
            </div>
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <div
                v-for="(item, index) in downloadHistory"
                :key="index"
                class="glass-subtle p-3 rounded-lg group hover:border-blue-400/30 transition-all"
              >
                <p class="text-xs text-gray-300 truncate">
                  {{ item.title }}
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ item.resolution }} • {{ formatDate(item.date) }}
                </p>
              </div>
            </div>
          </div>

          <!-- Info Card -->
          <div class="glass-subtle p-6">
            <h4 class="text-sm font-semibold text-white mb-3">ℹ️ How it works</h4>
            <ul class="text-xs text-gray-300 space-y-2">
              <li class="flex gap-2">
                <span class="text-blue-400">1.</span>
                <span>Paste a YouTube URL</span>
              </li>
              <li class="flex gap-2">
                <span class="text-blue-400">2.</span>
                <span>Choose your preferred resolution</span>
              </li>
              <li class="flex gap-2">
                <span class="text-blue-400">3.</span>
                <span>Click "Download Now" to start</span>
              </li>
              <li class="flex gap-2">
                <span class="text-blue-400">4.</span>
                <span>File saved as MP4 with auto audio merge</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000'

// Reactive state
const youtubeUrl = ref('')
const videoInfo = ref(null)
const selectedFormat = ref(null)
const loading = ref(false)
const downloading = ref(false)
const error = ref('')
const downloadProgress = ref(0)
const downloadSuccess = ref('')
const downloadHistory = ref([])

// Load history from localStorage
onMounted(() => {
  const saved = localStorage.getItem('downloadHistory')
  if (saved) {
    downloadHistory.value = JSON.parse(saved)
  }
})

// Fetch video formats
const fetchFormats = async () => {
  error.value = ''
  loading.value = true
  selectedFormat.value = null
  videoInfo.value = null
  downloadSuccess.value = ''

  try {
    const response = await axios.post(`${API_BASE_URL}/get-formats`, {
      url: youtubeUrl.value
    })

    videoInfo.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch video information. Please check the URL.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Download video
const downloadVideo = async () => {
  if (!selectedFormat.value || !videoInfo.value) return

  downloading.value = true
  downloadProgress.value = 0
  error.value = ''
  downloadSuccess.value = ''

  try {
    // Simulate progress
    const progressInterval = setInterval(() => {
      downloadProgress.value = Math.min(downloadProgress.value + Math.random() * 30, 90)
    }, 500)

    const response = await axios.post(`${API_BASE_URL}/download`, {
      url: youtubeUrl.value,
      format_id: selectedFormat.value.format_id
    })

    clearInterval(progressInterval)
    downloadProgress.value = 100

    if (response.data.status === 'success') {
      downloadSuccess.value = response.data.filename

      // Trigger browser download
      const downloadUrl = `${API_BASE_URL}/downloads/${response.data.filename}`
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = response.data.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      // Add to history
      const historyItem = {
        title: videoInfo.value.title,
        resolution: selectedFormat.value.resolution,
        date: new Date().toISOString(),
        filename: response.data.filename
      }
      downloadHistory.value.unshift(historyItem)
      localStorage.setItem('downloadHistory', JSON.stringify(downloadHistory.value.slice(0, 20)))

      // Reset after 3 seconds
      setTimeout(() => {
        youtubeUrl.value = ''
        videoInfo.value = null
        selectedFormat.value = null
        downloadProgress.value = 0
      }, 3000)
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Download failed. Please try again.'
    console.error(err)
  } finally {
    downloading.value = false
  }
}

// Clear download history
const clearHistory = () => {
  if (confirm('Are you sure you want to clear the download history?')) {
    downloadHistory.value = []
    localStorage.removeItem('downloadHistory')
  }
}

// Format duration
const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hours > 0) {
    return `${hours}h ${minutes}m ${secs}s`
  }
  return `${minutes}m ${secs}s`
}

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date

  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`

  return date.toLocaleDateString()
}
</script>

<style scoped>
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeInScale {
  animation: fadeInScale 0.4s ease-out;
}

@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
