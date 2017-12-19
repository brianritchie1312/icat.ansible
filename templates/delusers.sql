use {{ icat_name }}

delete from USER_ where NAME RLIKE "^db/user";
delete from USER_ where NAME = "{{ icat_admin_mech }}/{{ icat_admin_user }}";
