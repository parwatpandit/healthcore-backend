1. activate virtual machine
source venv/bin/activate

2. run backend
cd /Users/admin/Documents/HealthCore
source venv/bin/activate
python manage.py runserver

3. run frontend
cd /Users/admin/Documents/healthcore-frontend
npm run dev

4. git hub pushing 

path of the folder first==>cd /Users/admin/Documents/healthcore-frontend
==> git add .
==>git commit -m "feat(billing): add Phase 7 billing frontend

- Add Billing page with invoice table and status badges
- Add create invoice modal with dynamic line items
"
==>git push origin main



5. actual all bankend run by start.sh file 
backent ==> cd /Users/admin/Documents/HealthCore
python3 start.py

6. frontend
frontend ==> cd /Users/admin/Documents/healthcore-frontend
npm run dev

7. run both forntend and backend form docker
==> cd /Users/admin/Documents/HealthCore
docker-compose up
 
 open in browser:
 ==> http://localhost