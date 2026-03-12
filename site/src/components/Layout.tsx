import { NavLink, Outlet } from 'react-router-dom'

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
        <NavLink to="/analytics">Analytics</NavLink>
      </nav>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
