import { HashRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Timeline from './pages/Timeline'
import Exegesis from './pages/Exegesis'
import Essays from './pages/Essays'
import EssayDetail from './pages/EssayDetail'
import Theophanies from './pages/Theophanies'
import TheophanyDetail from './pages/TheophanyDetail'
import Browse from './pages/Browse'
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
import Bookmarks from './pages/Bookmarks'
import TagResults from './pages/TagResults'
import StudiesIndex from './pages/StudiesIndex'
import StudyIndex from './pages/StudyIndex'
import TopicDetail from './pages/TopicDetail'
import ScenesIndex from './pages/ScenesIndex'
import SceneDetail from './pages/SceneDetail'
import './App.css'

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="timeline" element={<Timeline />} />
          <Route path="timeline/:year" element={<Timeline />} />
          <Route path="exegesis" element={<Exegesis />} />
          <Route path="essays" element={<Essays />} />
          <Route path="essays/:slug" element={<EssayDetail />} />
          <Route path="theophanies" element={<Theophanies />} />
          <Route path="theophanies/:slug" element={<TheophanyDetail />} />
          <Route path="browse" element={<Browse />} />
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
          <Route path="bookmarks" element={<Bookmarks />} />
          <Route path="studies" element={<StudiesIndex />} />
          <Route path="studies/:studyId" element={<StudyIndex />} />
          <Route path="studies/:studyId/:slug" element={<TopicDetail />} />
          <Route path="studies/ai/scenes" element={<ScenesIndex />} />
          <Route path="studies/ai/scenes/:sceneId" element={<SceneDetail />} />
          <Route path="tag/:tagname" element={<TagResults />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
