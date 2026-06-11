import { useState, useEffect } from 'react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');

  const fetchNotes = () => {
    fetch(`${API}/notes`)
      .then(r => r.json())
      .then(setNotes)
      .catch(() => setError('Cannot reach backend'));
  };

  useEffect(() => { fetchNotes(); }, []);

  const addNote = () => {
    if (!title || !content) { setError('Both fields required'); return; }
    fetch(`${API}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    })
      .then(r => r.json())
      .then(() => { setTitle(''); setContent(''); setError(''); fetchNotes(); });
  };

  const deleteNote = (id) => {
    fetch(`${API}/notes/${id}`, { method: 'DELETE' })
      .then(() => fetchNotes());
  };

  return (
    <div style={{ maxWidth: 640, margin: '40px auto', fontFamily: 'sans-serif', padding: '0 16px' }}>
      <h1 style={{ fontSize: 24, marginBottom: 24 }}>NoteOps</h1>

      <div style={{ marginBottom: 24, padding: 16, border: '1px solid #ddd', borderRadius: 8 }}>
        <input
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          style={{ display: 'block', width: '100%', marginBottom: 8, padding: 8, boxSizing: 'border-box', borderRadius: 4, border: '1px solid #ccc' }}
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={e => setContent(e.target.value)}
          rows={3}
          style={{ display: 'block', width: '100%', marginBottom: 8, padding: 8, boxSizing: 'border-box', borderRadius: 4, border: '1px solid #ccc' }}
        />
        {error && <p style={{ color: 'red', margin: '0 0 8px' }}>{error}</p>}
        <button onClick={addNote} style={{ padding: '8px 20px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
          Add note
        </button>
      </div>

      {notes.map(note => (
        <div key={note.id} style={{ padding: 16, border: '1px solid #ddd', borderRadius: 8, marginBottom: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <strong>{note.title}</strong>
            <button onClick={() => deleteNote(note.id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#888', fontSize: 18 }}>×</button>
          </div>
          <p style={{ margin: '8px 0 0', color: '#555' }}>{note.content}</p>
          <small style={{ color: '#aaa' }}>{new Date(note.created_at).toLocaleString()}</small>
        </div>
      ))}
    </div>
  );
}

export default App;
