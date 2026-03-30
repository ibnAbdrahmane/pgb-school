# NEW TODO: Carte Login + Cartes View/Download + Absence Alerts

## Implementation Steps

### 1. Carte Login for Eleves
- [x] Edit app/routes/auth.py: Add numero_carte lookup in login()
- [x] Edit app/templates/auth/login.html: Add carte input/toggle

### 2. Admin/Scolarite Cartes List & Download
- [x] Edit app/routes/scolarite.py: Add /cartes route
- [x] Edit app/routes/admin.py: Add /cartes route
- [x] Create app/templates/scolarite/cartes.html
- [x] Create app/templates/admin/cartes.html
- [x] Add download_carte/<id> routes

### 3. Absence Alerts (>3 in 30 days)
- [ ] Read app/routes/eleve.py dashboard
- [ ] Add absence_count logic
- [ ] Update eleve/dashboard.html alert banner

### 4. Completion
- [ ] Test carte login
- [ ] Test cartes views/downloads
- [ ] Test absence alerts
- [ ] attempt_completion

Current: Step 1 complete, Step 2 cartes routes
