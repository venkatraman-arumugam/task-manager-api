const app = Vue.createApp({
  data() {
    return {
      taskNames: ["Write Report", "Analyze Data", "Fix Bug", "Update Docs", "Code Review"], // Predefined list of task names
      tasks: [], // List of all tasks
      currentPage: 1, // Current page number
      tasksPerPage: 10, // Maximum tasks per page
      totalTasks: 0, // Total number of tasks
      taskDetails: {}, // Task details by ID
      expandedTask: null, // Tracks the currently expanded task
    };
  },
  computed: {
    totalPages() {
      // Calculate total number of pages
      return Math.ceil(this.totalTasks / this.tasksPerPage);
    },
    paginatedTasks() {
      // Get tasks for the current page
      return this.tasks
    },
  },
  methods: {
   getRandomTaskName() {
      // Get a random name from the taskNames array
      const randomIndex = Math.floor(Math.random() * this.taskNames.length);
      return this.taskNames[randomIndex];
    },
    initializeNewTask() {
      // Generate a random task and set it to newTask
      const taskName = this.getRandomTaskName();
      const duration = Math.floor(Math.random() * 11) + 2; // Random duration between 1 and 10
      this.newTask = JSON.stringify({ task_name: taskName, duration }, null, 2);
    },
    async fetchTasks(page = 1) {
      try {
        const response = await fetch(`/tasks?page=${page}&page_size=${this.tasksPerPage}`);
        if (!response.ok) throw new Error("Failed to fetch tasks.");

        const data = await response.json();
        this.tasks = data.tasks;
        this.totalTasks = data.pagination.total_tasks;
        this.currentPage = data.pagination.current_page;
      } catch (error) {
        console.error("Error fetching tasks:", error);
        alert("Failed to fetch tasks. Please try again.");
      }
    },
    async createTask() {
      try {
        // Check if the current page is full
        const currentPageTasks = this.paginatedTasks.length;
        if (currentPageTasks >= this.tasksPerPage) {
          this.currentPage += 1; // Move to the next page
        }

        // Create a new task
        const response = await fetch("/tasks", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: this.newTask,
        });

        if (response.ok) {
          this.fetchTasks(this.currentPage); // Refresh tasks for the current page
          this.initializeNewTask();
        } else {
          throw new Error("Failed to create task.");
        }
      } catch (error) {
        console.error("Error creating task:", error);
        alert("Failed to create task. Please try again.");
      }
    },
    toggleDetails(index) {
      // Expand or collapse task details
      this.expandedTask = this.expandedTask === index ? null : index;
    },
    async triggerTask(taskId) {
      try {
        const response = await fetch(`/tasks/${taskId}`);
        if (!response.ok) throw new Error("Failed to fetch task details.");

        const data = await response.json();
        this.taskDetails = { ...this.taskDetails, [taskId]: data }; // Update task details reactively
      } catch (error) {
        console.error("Error fetching task details:", error);
        alert("Failed to fetch task details. Please try again.");
      }
    },
    statusClass(status) {
      // Return CSS class based on task status
      return {
        "text-success": status === "COMPLETED",
        "text-warning": status === "PROCESSING",
        "text-danger": status === "FAILED",
        "text-secondary": status === "QUEUED",
      }[status];
    },
    navigateToPage(page) {
      // Navigate to a specific page
      if (page >= 1 && page <= this.totalPages) {
        this.fetchTasks(page);
      }
    },
  },
  mounted() {
    // Fetch tasks when the app is mounted
    this.initializeNewTask();
    this.fetchTasks();
  },
});

app.mount("#app");
