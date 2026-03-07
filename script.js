const supabaseUrl = 'https://wpyixlovraikzufifjhe.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndweWl4bG92cmFpa3p1ZmlmamhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI4NzUzNjUsImV4cCI6MjA4ODQ1MTM2NX0.AnmM-tVpVYGFCe42NozutnjU9rrTb7KMtBMjrESr4_Y';
const supabase = supabase.createClient(supabaseUrl, supabaseKey);

// DOM elements
const form = document.getElementById("add-word-form");
const wordList = document.getElementById("word-list");

// Form submission handling
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form from reloading the page

    const word = document.getElementById("word").value;
    const definition = document.getElementById("definition").value;
    const link = document.getElementById("link").value;

    // Validate form fields
    if (!word || !definition || !link) {
        alert("All fields must be filled out!");
        return;
    }

    // Insert new word into Supabase
    const { data, error } = await supabase
        .from('dictionary')
        .insert([
            { word: word, definition: definition, link: link }
        ]);

    if (error) {
        console.error('Error inserting data:', error.message);
        alert("Error inserting data: " + error.message);
    } else {
        console.log('Inserted data:', data);
        loadWords();  // Reload words after insertion
    }
});

// Load all words from the database
async function loadWords() {

    console.log("Loading words...");
    
    const { data, error } = await supabase
        .from('dictionary')
        .select('*');

    if (error) {
        console.error('Error loading data:', error.message);
        alert("Error loading data: " + error.message);
    } else {
        // Clear the word list
        wordList.innerHTML = '';
        
        // Populate the word list
        data.forEach(wordData => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${wordData.word}</strong><br>${wordData.definition}<br><a href="${wordData.link}" target="_blank">${wordData.link}</a>`;
            wordList.appendChild(li);
        });
    }
}

// Load words on page load
loadWords();
