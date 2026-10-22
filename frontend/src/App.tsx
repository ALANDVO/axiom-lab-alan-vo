import { DictionaryPage } from './pages/DictionaryPage';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">freehire</div>
        <nav className="nav">
          <a href="/dictionary">Dictionary</a>
          <a href="/jobs">Jobs</a>
          <a href="/profile">Profile</a>
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer>
      <p>freehire — Open-source search engine for job seekers</p>
      <p>Alan Vo alanvo@gmail.com</p>
    </footer>
  );
}

function App() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ flex: 1 }}>
        <DictionaryPage />
      </main>
      <Footer />
    </div>
  );
}

export default App;