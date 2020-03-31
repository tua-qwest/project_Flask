import datetime
from flask import Flask, redirect, request, render_template, abort
from data import db_session, register, users, login_form, group, group_form, student, student_form, answer, answer_form
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    if current_user.is_authenticated:
        gr = session.query(group.Group).filter(group.Group.user == current_user)
    else:
        gr = []
    return render_template("index.html", groups=gr)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = register.RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form.LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/groups',  methods=['GET', 'POST'])
@login_required
def add_group():
    form = group_form.GroupForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        gr = group.Group()
        gr.group_name = form.group_name.data
        gr.id_user = current_user.id
        session.add(gr)
        session.commit()
        return redirect('/')
    return render_template('groups.html', title='Добавление класса', form=form)


@app.route('/group/<int:id>', methods=['GET', 'POST'])
@login_required
def group_show(id):
    session = db_session.create_session()
    gr = session.query(group.Group).filter(group.Group.id == id).first()
    st = session.query(student.Student).filter(student.Student.id_group == id).all()

    return render_template('students.html', title=f'Список класса {gr.group_name}',
                           st=st, id=id)


@app.route('/group_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = group_form.GroupForm()
    if request.method == "GET":
        session = db_session.create_session()
        gr = session.query(group.Group).filter(group.Group.id == id).first()
        if gr:
            form.group_name.data = gr.group_name
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        gr = session.query(group.Group).filter(group.Group.id == id).first()
        if gr:
            gr.group_name = form.group_name.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('groups.html', title='Редактирование класса', form=form)


@app.route('/group_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    gr = session.query(group.Group).filter(group.Group.id == id).first()
    if gr:
        session.delete(gr)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/group/student_add/<int:id>',  methods=['GET', 'POST'])
@login_required
def add_student(id):
    form = student_form.StudentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        st = student.Student()
        st.surname = form.surname.data
        st.first_name = form.first_name.data
        st.last_name = form.last_name.data
        st.id_group = id
        session.add(st)
        session.commit()
        return redirect(f'/group/{id}')
    return render_template('student_form.html', title='Добавление ученика', form=form)


@app.route('/student_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def student_edit(id):
    form = student_form.StudentForm()
    if request.method == "GET":
        session = db_session.create_session()
        st = session.query(student.Student).filter(student.Student.id == id).first()
        if st:
            form.surname.data = st.surname
            form.first_name.data = st.first_name
            form.last_name.data = st.last_name
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        st = session.query(student.Student).filter(student.Student.id == id).first()
        if st:
            st.surname = form.surname.data
            st.first_name = form.first_name.data
            st.last_name = form.last_name.data
            session.commit()
            return redirect(f'/group/{st.id_group}')
        else:
            abort(404)
    return render_template('student_form.html', title='Редактирование ученика', form=form)


@app.route('/student_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def student_delete(id):
    session = db_session.create_session()
    st = session.query(student.Student).filter(student.Student.id == id).first()
    group_id = st.id_group
    if st:
        session.delete(st)
        session.commit()
    else:
        abort(404)
    return redirect(f'/group/{group_id}')


@app.route('/answers/<int:id>', methods=['GET', 'POST'])
@login_required
def answers(id):

    session = db_session.create_session()
    gr = session.query(group.Group).filter(group.Group.id == id).first()
    st = session.query(student.Student).filter(student.Student.id_group == id).all()
    answ_list = []
    for s in st:
        answ_list.append(session.query(answer.Answer).
                         filter(answer.Answer.id_student == s.id,
                                answer.Answer.date == datetime.datetime.now().date()).first())
    return render_template('mark.html', title=f'Список класса {gr.group_name}', st=st, id=id,
                           lst=answ_list)


@app.route('/answer_add/<int:id>',  methods=['GET', 'POST'])
@login_required
def answer_add(id):
    st = ''
    form = answer_form.MarkForm()
    session = db_session.create_session()
    st = session.query(student.Student).filter(student.Student.id == id).first()
    if form.validate_on_submit():
        mr = answer.Answer()
        mr.date = form.date.data
        if mr.date == '':
            mr.date = None
        else:
            mr.date = datetime.datetime.strptime(form.date.data, '%Y-%m-%d')
        mr.mark = form.mark.data
        mr.id_student = id
        session.add(mr)
        session.commit()
        return redirect(f'/answers/{st.id_group}')
    return render_template('mark_add.html', title='Добавление оценки', form=form, st=st)


@app.route('/answer_view/<int:id>',  methods=['GET', 'POST'])
@login_required
def answer_view(id):
    session = db_session.create_session()
    mr = session.query(answer.Answer).filter(answer.Answer.id_student == id).order_by(
        answer.Answer.date.desc())
    st = session.query(student.Student).filter(student.Student.id == id).first()
    return render_template('mark_view.html', title='Просмотр оценок', mr=mr, st=st)


@app.route('/answer_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def answer_delete(id):
    session = db_session.create_session()
    mr = session.query(answer.Answer).filter(answer.Answer.id == id).first()
    st_id = mr.id_student
    if mr:
        session.delete(mr)
        session.commit()
    else:
        abort(404)
    return redirect(f'/answer_view/{st_id}')


def main():
    db_session.global_init("db/edu.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
