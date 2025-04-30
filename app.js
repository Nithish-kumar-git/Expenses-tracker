document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const loginPage = document.getElementById('login-page');
    const mainApp = document.getElementById('main-app');
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const generatePasswordBtn = document.getElementById('generate-password');
    const logoutBtn = document.getElementById('logout-btn');
  
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page-content');
  
    const totalIncomeEl = document.getElementById('total-income');
    const totalExpensesEl = document.getElementById('total-expenses');
    const balanceEl = document.getElementById('balance');
  
    const incomeForm = document.getElementById('income-form');
    const incomeDescriptionInput = document.getElementById('income-description');
    const incomeAmountInput = document.getElementById('income-amount');
    const incomeList = document.getElementById('income-list');
  
    const expensesForm = document.getElementById('expenses-form');
    const expenseDescriptionInput = document.getElementById('expense-description');
    const expenseAmountInput = document.getElementById('expense-amount');
    const expensesList = document.getElementById('expenses-list');
  
    const transactionList = document.getElementById('transaction-list');
  
    // Data keys for localStorage
    const STORAGE_KEY = 'budgetAppData';
    const USER_KEY = 'budgetAppUser';
  
    // State
    let budgetData = {
      income: [],
      expenses: [],
    };
  
    let currentUser = null;
  
    // --- Password Generator ---
    function generatePassword(length = 12) {
      const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}:"<>?|[];\',./`~';
      let password = '';
      for (let i = 0; i < length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return password;
    }
  
    generatePasswordBtn.addEventListener('click', () => {
      const newPassword = generatePassword();
      passwordInput.value = newPassword;
    });
  
    // --- Login Logic ---
    loginForm.addEventListener('submit', e => {
      e.preventDefault();
      const username = usernameInput.value.trim();
      const password = passwordInput.value;
  
      if (!username || !password) {
        alert('Please enter both username and password.');
        return;
      }
  
      // For demo: simple login, store user in localStorage
      currentUser = username;
      localStorage.setItem(USER_KEY, currentUser);
  
      loadBudgetData();
      showMainApp();
    });
  
    // --- Logout Logic ---
    logoutBtn.addEventListener('click', () => {
      currentUser = null;
      localStorage.removeItem(USER_KEY);
      budgetData = { income: [], expenses: [] };
      clearInputs();
      showLoginPage();
    });
  
    // --- Show / Hide Pages ---
    function showLoginPage() {
      loginPage.classList.add('active');
      mainApp.classList.add('hidden');
      mainApp.classList.remove('active');
      clearInputs();
    }
  
    function showMainApp() {
      loginPage.classList.remove('active');
      mainApp.classList.remove('hidden');
      mainApp.classList.add('active');
      setActivePage('budget-summary');
      renderAll();
    }
  
    function setActivePage(pageId) {
      pages.forEach(page => {
        page.classList.toggle('active', page.id === pageId);
      });
      navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageId);
      });
    }
  
    // Navigation clicks
    navLinks.forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const pageId = link.dataset.page;
        setActivePage(pageId);
      });
    });
  
    // --- Data Persistence ---
    function saveBudgetData() {
      if (!currentUser) return;
      localStorage.setItem(STORAGE_KEY + '_' + currentUser, JSON.stringify(budgetData));
    }
  
    function loadBudgetData() {
      if (!currentUser) return;
      const data = localStorage.getItem(STORAGE_KEY + '_' + currentUser);
      if (data) {
        budgetData = JSON.parse(data);
      } else {
        budgetData = { income: [], expenses: [] };
      }
    }
  
    // --- Render Functions ---
    function renderAll() {
      renderSummary();
      renderIncomeList();
      renderExpensesList();
      renderTransactionHistory();
    }
  
    function renderSummary() {
      const totalIncome = budgetData.income.reduce((sum, item) => sum + item.amount, 0);
      const totalExpenses = budgetData.expenses.reduce((sum, item) => sum + item.amount, 0);
      const balance = totalIncome - totalExpenses;
  
      totalIncomeEl.textContent = totalIncome.toFixed(2) + ' USD';
      totalExpensesEl.textContent = totalExpenses.toFixed(2) + ' USD';
      balanceEl.textContent = balance.toFixed(2) + ' USD';
    }
  
    function renderIncomeList() {
      incomeList.innerHTML = '';
      if (budgetData.income.length === 0) {
        incomeList.innerHTML = '<li>No income entries</li>';
        return;
      }
      budgetData.income.forEach((item, index) => {
        const li = document.createElement('li');
        li.className = 'income';
        li.textContent = `${item.description} - ${item.amount.toFixed(2)} USD`;
        // Add delete button
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.className = 'delete-btn';
        delBtn.addEventListener('click', () => {
          budgetData.income.splice(index, 1);
          saveBudgetData();
          renderAll();
        });
        li.appendChild(delBtn);
        incomeList.appendChild(li);
      });
    }
  
    function renderExpensesList() {
      expensesList.innerHTML = '';
      if (budgetData.expenses.length === 0) {
        expensesList.innerHTML = '<li>No expense entries</li>';
        return;
      }
      budgetData.expenses.forEach((item, index) => {
        const li = document.createElement('li');
        li.className = 'expense';
        li.textContent = `${item.description} - ${item.amount.toFixed(2)} USD`;
        // Add delete button
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.className = 'delete-btn';
        delBtn.addEventListener('click', () => {
          budgetData.expenses.splice(index, 1);
          saveBudgetData();
          renderAll();
        });
        li.appendChild(delBtn);
        expensesList.appendChild(li);
      });
    }
  
    function renderTransactionHistory() {
      transactionList.innerHTML = '';
      const allTransactions = [
        ...budgetData.income.map(i => ({ ...i, type: 'income' })),
        ...budgetData.expenses.map(e => ({ ...e, type: 'expense' })),
      ];
      if (allTransactions.length === 0) {
        transactionList.innerHTML = '<li>No transactions</li>';
        return;
      }
      // Sort by date descending (newest first)
      allTransactions.sort((a, b) => b.date - a.date);
  
      allTransactions.forEach(item => {
        const li = document.createElement('li');
        li.className = item.type === 'income' ? 'income' : 'expense';
        const dateStr = new Date(item.date).toLocaleDateString('en-US');
        li.textContent = `[${dateStr}] ${item.description} - ${item.amount.toFixed(2)} USD`;
        transactionList.appendChild(li);
      });
    }
  
    // --- Add Income ---
    incomeForm.addEventListener('submit', e => {
      e.preventDefault();
      const description = incomeDescriptionInput.value.trim();
      const amount = parseFloat(incomeAmountInput.value);
      if (!description || isNaN(amount) || amount <= 0) {
        alert('Please enter a valid income description and amount.');
        return;
      }
      budgetData.income.push({
        description,
        amount,
        date: Date.now(),
      });
      saveBudgetData();
      incomeDescriptionInput.value = '';
      incomeAmountInput.value = '';
      renderAll();
    });
  
    // --- Add Expense ---
    expensesForm.addEventListener('submit', e => {
      e.preventDefault();
      const description = expenseDescriptionInput.value.trim();
      const amount = parseFloat(expenseAmountInput.value);
      if (!description || isNaN(amount) || amount <= 0) {
        alert('Please enter a valid expense description and amount.');
        return;
      }
      budgetData.expenses.push({
        description,
        amount,
        date: Date.now(),
      });
      saveBudgetData();
      expenseDescriptionInput.value = '';
      expenseAmountInput.value = '';
      renderAll();
    });
  
    // --- Clear inputs on logout ---
    function clearInputs() {
      usernameInput.value = '';
      passwordInput.value = '';
      incomeDescriptionInput.value = '';
      incomeAmountInput.value = '';
      expenseDescriptionInput.value = '';
      expenseAmountInput.value = '';
      incomeList.innerHTML = '';
      expensesList.innerHTML = '';
      transactionList.innerHTML = '';
      totalIncomeEl.textContent = '0 USD';
      totalExpensesEl.textContent = '0 USD';
      balanceEl.textContent = '0 USD';
    }
  
    // --- Auto-login if user saved ---
    window.addEventListener('load', () => {
      const savedUser = localStorage.getItem(USER_KEY);
      if (savedUser) {
        currentUser = savedUser;
        loadBudgetData();
        showMainApp();
      } else {
        showLoginPage();
      }
    });
  });
  