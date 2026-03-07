const supabaseUrl = 'https://wpyixlovraikzufifjhe.supabase.co';
const supabaseKey = 'sb_publishable_iOqaoNTp-8QSRshFhtRV2Q_AbwyOY09';
const supabase = supabase.createClient(supabaseUrl, supabaseKey);

const form = document.getElementById("add-word-form");
const wordList = document.getElementById("word-list");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const word = document.getElementById("word").value;
    const definition = document.getElementById("definition").value;
    const link = document.getElementById("link").value;

    // Insert new word into Supabase
    const { data, error } = await supabase
        .from('dictionary')
        .insert([
            { word: word, definition: definition, link: link }
        ]);

    if (error) {
        console.error('Error inserting data:', error);
    } else {
        loadWords();
    }
});

// Load all words from the database
async function loadWords() {
    const { data, error } = await supabase
        .from('dictionary')
        .select('*');

    if (error) {
        console.error('Error loading data:', error);
    } else {
        wordList.innerHTML = '';
        data.forEach(wordData => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${wordData.word}</strong><br>${wordData.definition}<br><a href="${wordData.link}" target="_blank">${wordData.link}</a>`;
            wordList.appendChild(li);
        });
    }
}

// Load words on page load
loadWords();
