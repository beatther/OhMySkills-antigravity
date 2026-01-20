import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import SkillList from './pages/SkillList'
import SkillDetail from './pages/SkillDetail'
import './App.css'

function App() {
    return (
        <div className="app">
            <Header />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/skills" element={<SkillList />} />
                    <Route path="/skill/:id" element={<SkillDetail />} />
                </Routes>
            </main>
        </div>
    )
}

export default App
