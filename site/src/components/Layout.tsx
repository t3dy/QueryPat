import { NavLink, Outlet } from 'react-router-dom'
import Breadcrumbs from './Breadcrumbs'

export default function Layout() {
  return (
    <div className="app-layout">
      <nav className="app-nav">
        <span className="nav-brand">PKD Knowledge Portal</span>
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/browse">Browse</NavLink>
        <NavLink to="/biography">Biography</NavLink>
        <NavLink to="/map">Map</NavLink>
        <NavLink to="/people">People</NavLink>
        <NavLink to="/works">Works</NavLink>
        <NavLink to="/themes">Themes</NavLink>
        <NavLink to="/pkd-on-pkd">PKD on PKD</NavLink>
        <NavLink to="/timeline">Timeline</NavLink>
        <NavLink to="/exegesis">Exegesis</NavLink>
        <NavLink to="/theophanies">Theophanies</NavLink>
        <NavLink to="/paranormal">Paranormal</NavLink>
        <NavLink to="/archive">Archive</NavLink>
        <NavLink to="/dictionary">Dictionary</NavLink>
        <NavLink to="/names">Names</NavLink>
        <NavLink to="/scholars">Scholars</NavLink>
        <NavLink to="/essays">Essays</NavLink>
        <NavLink to="/studies">Studies</NavLink>
        <NavLink to="/search">Search</NavLink>
        <NavLink to="/bookmarks">Bookmarks</NavLink>
      </nav>
      <main className="app-main">
        <Breadcrumbs />
        <Outlet />
      </main>
    </div>
  )
}
