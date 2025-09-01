const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL('http://localhost:3000');
}

app.whenReady().then(() => {
  createWindow();

  ipcMain.on('save-journal', (event, journalData) => {
    console.log('Received save-journal message');

    const options = {
      args: [JSON.stringify(journalData)]
    };

    PythonShell.run('../task_journal/journal_processor.py', options).then(results => {
      console.log('Python script finished.');
      console.log('results: ', results);
      // results is an array of strings, each a line of stdout
      // I expect a single line of JSON
      try {
          const response = JSON.parse(results[0]);
          event.reply('save-journal-reply', response);
      } catch(e) {
          event.reply('save-journal-reply', {success: false, message: 'Failed to parse python response'});
      }
    });
  });

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
