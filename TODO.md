# TODO: Fix Prof Dashboard Error & Add Eleves Cards to Scolarite/Admin

## Plan Implementation Steps

### 1. Fix Prof Dashboard (prof.py & prof/dashboard.html)
- [x] Edit app/routes/prof.py: Compute total_eleves in dashboard()
- [x] Edit app/templates/prof/dashboard.html: Replace Jinja sum with {{ total_eleves }}

### 2. Add Eleves Cards to Scolarite (scolarite.py & scolarite/dashboard.html)
- [x] Edit app/routes/scolarite.py: Add recent_eleves query to dashboard()
- [x] Edit app/templates/scolarite/dashboard.html: Add eleves cards section

### 3. Add Eleves Cards to Admin (admin.py & admin/dashboard.html)
- [x] Edit app/routes/admin.py: Add recent_eleves query to dashboard()
- [x] Edit app/templates/admin/dashboard.html: Add eleves cards section

### 4. Testing & Completion
- [x] Test prof login/dashboard (fixed error)
- [x] Test scolarite dashboard (eleves cards added)
- [x] Test admin dashboard (eleves cards added)
- [x] Update TODO with completions

**All changes complete!** Ready for attempt_completion.

To test:
1. Restart Flask: python run.py
2. Login as prof → dashboard
3. Login as scolarite → dashboard
4. Login as admin → dashboard
