const API_URL = "http://localhost:5000";
const SOCKET_URL = "ws://localhost:5000";
const el = (id) => document.getElementById(id);

// naglowki do zapytan jak juz sie zalogujesz
function tokenHeader() {
  const t = localStorage.getItem('token');
  return {'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'};
}

// przelaczenie zakladek miedzy publicznym czatem, wiadomosciami prywatnymi a forum
// function setActiveTab(name) {
//   document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
//   document.querySelectorAll('.tabpane').forEach(p => p.classList.add('hidden'));
//   document.querySelector(`.tab[data-tab="${name}"]`).classList.add('active');
//   el(`tab-${name}`).classList.remove('hidden');
// }

document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => setActiveTab(btn.dataset.tab));
});

// rejestracja
// el('register-form').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const username = el('reg-username').value;
//   const password = el('reg-password').value;

//   const r = await fetch(`${API_URL}/api/register`, {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({username, password})
//   });
//   const data = await r.json();
//   if (r.status !== 201) alert(data.error || 'Rejestracja nieudana');
//   else {
//     alert('Rejestracja udana! Zaloguj się.');
//     el('register-section').style.display = 'none';
//   }
// });


// logowanie sie do apki
// el('login-form').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const username = el('login-username').value;
//   const password = el('login-password').value;

//   const r = await fetch(`${API_URL}/api/login`, {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({username, password})
//   });
//   const data = await r.json();
//   if (r.status !== 200) {
//     alert(data.error || 'Logowanie nieudane');
//     return;
//   }

//   //zapisanie tokenu i nazwy urzytkownika 
//   localStorage.setItem('token', data.token);
//   localStorage.setItem('username', data.user.username);

//   // przejscie z ekranu logowania do apki
//   el('auth-section').style.display = 'none';
//   el('app-section').style.display = 'block';
//   el('welcome').innerText = `Witaj, ${data.user.username}!`;


  //odswieżenie danych po raz pierwszy
//   await refreshUsers(true);
//   await refreshPublic();
//   await refreshDM(true);
//   await refreshPosts();

//   // co 5s odśwież users + DM + public
//   // clearInterval(window.publicInterval);
//   connectSocket();
//   clearInterval(window.dmInterval);
//   clearInterval(window.forumInterval);

//   // window.publicInterval = setInterval(refreshPublic, 5000);
//   window.dmInterval = setInterval(async () => { await refreshUsers(false); await refreshDM(false); }, 5000);
//   window.forumInterval = setInterval(refreshPosts, 7000);
// });

async function connectSocket() {
  var socket = new WebSocket(SOCKET_URL);

  socket.addEventListener("open", (event) => {
    socket.send("test");
  });
}


//wylogowywanie
// el('logout-btn').addEventListener('click', () => {
//   localStorage.removeItem('token');
//   localStorage.removeItem('username');
//   el('app-section').style.display = 'none';
//   el('auth-section').style.display = 'block';
//   clearInterval(window.publicInterval);
//   clearInterval(window.dmInterval);
//   clearInterval(window.forumInterval);
// });

// ----- USERS (lista pozniej do prywatnych wiadomosci DM) -----
// async function refreshUsers(forceSelectFirst) {
//   const r = await fetch(`${API_URL}/api/users`);
//   const users = await r.json();
//   const me = localStorage.getItem('username');
//   const sel = el('dm-user');

//   const prev = sel.value;
//   sel.innerHTML = '';

//   //w dm pokazuje kazdego opocz mnie
//   const others = users.filter(u => u !== me);
//   others.forEach(u => {
//     const opt = document.createElement('option');
//     opt.value = u;
//     opt.textContent = u;
//     sel.appendChild(opt);
//   });

//   // zachowaj wybór jeśli się da
//   if (others.includes(prev)) sel.value = prev;
//   else if (forceSelectFirst && others.length > 0) sel.value = others[0];
// }

// ----- PUBLICZNY CHAT -----
// async function refreshPublic() {
//   const r = await fetch(`${API_URL}/api/public/messages`);
//   const list = await r.json();
//   const box = el('public-messages');
//   box.innerHTML = '';
//   list.forEach(m => {
//     const p = document.createElement('div');
//     p.className = 'msg';
//     p.textContent = `${m.timestamp} - ${m.username}: ${m.content}`;
//     box.appendChild(p);
//   });
//   box.scrollTop = box.scrollHeight;
// }

// el('public-form').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const content = el('public-input').value;
//   const r = await fetch(`${API_URL}/api/public/messages`, {
//     method: 'POST',
//     headers: tokenHeader(),
//     body: JSON.stringify({content})
//   });
//   const data = await r.json();
//   if (r.status !== 201) alert(data.error || 'Błąd');
//   else {
//     el('public-input').value = '';
//     await refreshPublic();
//   }
// });

// ----- PRIVATE (DM) -----
async function refreshDM(forceTrySelectFirst) {
  const sel = el('dm-user');
  if (!sel) return;

  //jesli nie ma wybranego usera
  if (!sel.value && forceTrySelectFirst) {
    await refreshUsers(true);
  }
  if (!sel.value) return;

  const withUser = encodeURIComponent(sel.value);
  const r = await fetch(`${API_URL}/api/private/messages?with=${withUser}`, {
    headers: tokenHeader()
  });
  const data = await r.json();

  const box = el('dm-messages');
  box.innerHTML = '';

  if (r.status !== 200) {
    const p = document.createElement('div');
    p.className = 'msg';
    p.textContent = data.error || 'Błąd pobierania DM';
    box.appendChild(p);
    return;
  }

  data.forEach(m => {
    const p = document.createElement('div');
    p.className = 'msg';
    p.textContent = `${m.timestamp} - ${m.from}: ${m.content}`;
    box.appendChild(p);
  });
  box.scrollTop = box.scrollHeight;
}

el('dm-user').addEventListener('change', () => refreshDM(false));
el('dm-refresh').addEventListener('click', () => refreshDM(true));

el('dm-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const to = el('dm-user').value;
  const content = el('dm-input').value;

  const r = await fetch(`${API_URL}/api/private/messages`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({to, content})
  });
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Błąd wysyłania');
  else {
    el('dm-input').value = '';
    await refreshDM(false);
  }
});

// ----- FORUM: posty + komentarze + reakcje -----
const EMOJIS = ["👍","❤️","😂","😮","😡"];

async function toggleReaction(postId, emoji) {
  const r = await fetch(`${API_URL}/api/forum/reactions`, {
    method: 'POST',
    headers: tokenHeader(),
    body: JSON.stringify({post_id: postId, emoji})
  });
  const data = await r.json();
  if (r.status !== 200) alert(data.error || 'Błąd reakcji');
  await refreshPosts();
}

// async function addComment(postId, body) {
//   const r = await fetch(`${API_URL}/api/forum/comments`, {
//     method: 'POST',
//     headers: tokenHeader(),
//     body: JSON.stringify({post_id: postId, body})
//   });
//   const data = await r.json();
//   if (r.status !== 201) alert(data.error || 'Błąd komentarza');
//   await refreshPosts();
// }

// async function refreshPosts() {
//   const r = await fetch(`${API_URL}/api/forum/posts`);
//   const posts = await r.json();
//   const box = el('posts');
//   box.innerHTML = '';

//   posts.forEach(p => {
//     const card = document.createElement('div');
//     card.className = 'post';

//     const h = document.createElement('div');
//     h.className = 'post-title';
//     h.textContent = p.title;

//     const meta = document.createElement('div');
//     meta.className = 'post-meta';
//     meta.textContent = `${p.timestamp} • ${p.author}`;

//     const body = document.createElement('div');
//     body.className = 'post-body';
//     body.textContent = p.body;

//     //reakcje
//     const reactRow = document.createElement('div');
//     reactRow.className = 'react-row';

//     EMOJIS.forEach(em => {
//       const btn = document.createElement('button');
//       btn.type = "button";
//       btn.className = "emoji";
//       const count = (p.reactions && p.reactions[em]) ? p.reactions[em] : 0;
//       btn.textContent = `${em} ${count}`;
//       btn.addEventListener('click', () => toggleReaction(p.id, em));
//       reactRow.appendChild(btn);
//     });

//     //lista komentarzy
//     const commBox = document.createElement('div');
//     commBox.className = 'comments';

//     (p.comments || []).forEach(c => {
//       const line = document.createElement('div');
//       line.className = 'comment';
//       line.textContent = `${c.timestamp} - ${c.author}: ${c.body}`;
//       commBox.appendChild(line);
//     });

//     //dodawanie komentarza
//     const form = document.createElement('form');
//     form.className = 'row';
//     form.innerHTML = `
//       <input type="text" class="comment-input" placeholder="Dodaj komentarz..." required />
//       <button type="submit">Dodaj</button>
//     `;
//     form.addEventListener('submit', async (e) => {
//       e.preventDefault();
//       const inp = form.querySelector('.comment-input');
//       const txt = inp.value;
//       inp.value = '';
//       await addComment(p.id, txt);
//     });

//     card.appendChild(h);
//     card.appendChild(meta);
//     card.appendChild(body);
//     card.appendChild(reactRow);

//     const commTitle = document.createElement('div');
//     commTitle.className = 'comm-title';
//     commTitle.textContent = 'Komentarze:';
//     card.appendChild(commTitle);

//     card.appendChild(commBox);
//     card.appendChild(form);

//     box.appendChild(card);
//   });
// }

// el('post-form').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const title = el('post-title').value;
//   const body = el('post-body').value;

//   const r = await fetch(`${API_URL}/api/forum/posts`, {
//     method: 'POST',
//     headers: tokenHeader(),
//     body: JSON.stringify({title, body})
//   });
//   const data = await r.json();
//   if (r.status !== 201) alert(data.error || 'Błąd dodania posta');
//   else {
//     el('post-title').value = '';
//     el('post-body').value = '';
//     await refreshPosts();
//     setActiveTab('forum');
//   }
// });
