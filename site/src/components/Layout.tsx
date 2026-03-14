import { NavLink, Outlet } from 'react-router-dom'
import Breadcrumbs from './Breadcrumbs'

export default function Layout() {
  return (
    <div className="app-layout">
      <nav className="app-nav">
        <span className="nav-brand">QueryPat</span>
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/timeline">Timeline</NavLink>
        <NavLink to="/dictionary">Dictionary</NavLink>
        <NavLink to="/archive">Archive</NavLink>
        <NavLink to="/search">Search</NavLink>
        <NavLink to="/biography">Biography</NavLink>
        <NavLink to="/scholars">Scholars</NavLink>
        <NavLink to="/names">Names</NavLink>
        <NavLink to="/bookmarks">Bookmarks</NavLink>
      </nav>
      <main className="app-main">
        <Breadcrumbs />
        <Outlet />
      </main>
    </div>
  )
}
