const supabaseUrl = 'https://wpyixlovraikzufifjhe.supabase.co';
const supabaseKey = 'sb_publishable_iOqaoNTp-8QSRshFhtRV2Q_AbwyOY09';
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
