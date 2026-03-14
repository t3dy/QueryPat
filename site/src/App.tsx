import { HashRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Timeline from './pages/Timeline'
import SegmentDetail from './pages/SegmentDetail'
import Dictionary from './pages/Dictionary'
import TermDetail from './pages/TermDetail'
import Archive from './pages/Archive'
import ArchiveDetail from './pages/ArchiveDetail'
import Search from './pages/Search'
import Analytics from './pages/Analytics'
import Biography from './pages/Biography'
import Scholars from './pages/Scholars'
import Names from './pages/Names'
import NameDetail from './pages/NameDetail'
import './App.css'

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="timeline" element={<Timeline />} />
          <Route path="timeline/:year" element={<Timeline />} />
          <Route path="segments/:id" element={<SegmentDetail />} />
          <Route path="dictionary" element={<Dictionary />} />
          <Route path="dictionary/:slug" element={<TermDetail />} />
          <Route path="archive" element={<Archive />} />
          <Route path="archive/:slug" element={<ArchiveDetail />} />
          <Route path="search" element={<Search />} />
          <Route path="biography" element={<Biography />} />
          <Route path="scholars" element={<Scholars />} />
          <Route path="names" element={<Names />} />
          <Route path="names/:slug" element={<NameDetail />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
