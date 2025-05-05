#!!!!!i wrote it in the integrated terminal!!!!! i just copy pasted some of it to this file

from application import app,db
from application import Member,Orders,Course
from datetime import date


#with app.app_context():
    #maps the classes and creates it (if not exists)
    #db.create_all()


    #Insert data
    #andrew = Member(username='andrew',password='secret',email='andrew@msn.com',join_date=date.today())
    #michelle = Member(username='michelle',password='secret2',email='michelle@hotmail.com',join_date=date.today())
    #balint = Member(username='balint',password='secret3',email='balint@yahoo.com',join_date=date.today())
    #zsiga = Member(username='zsiga',password='biga',email='zsiga@citromail.hu',join_date=date.today())
    #dani = Member(username='dani',password='danyi',email='dani@freemail.hu',join_date=date.today())
    #keanu = Member(username='keanu',password='zawarudo',email='keanu@aol.com',join_date=date.today())
    
    #db.session.add(andrew)
    #db.session.add(michelle)
    #db.session.add(balint)
    #db.session.add(zsiga)
    #db.session.add(dani)
    #db.session.add(keanu)
    #db.session.commit()


    #Update data
    #andrew = Member.query.filter_by(username='andrew').first()
    #andrew.password = 'newsecretpassword'
    #db.session.commit()
    
    #michelle = Member.query.filter_by(username='michelle').first()
    #michelle.email = 'michelle@citromail.hu'
    #db.session.commit()
    
    
    #Delete data
    #db.session.delete(michelle)
    #db.session.commit()
    
    
    #Queries
    #results = Member.query.all()
    #andrew = Member.query.filter_by(username='andrew').first()
    #with just the filter i can use python code to filter
    #michelle = Member.query.filter(Member.username == 'michelle').first()
    
    #q = Member.query
    #q2 = q.filter(Member.username == 'andrew')
    #print(q.all())
    #print(q2.all())
    #
    #q  = Member.query.filter(Member.username.in_(['andrew','michelle'])).all()
    #
    #print(q)
    ## ~ == bitwise NOT (invert) operator  It flips all bits of an integer ex.: ~5 = -6, because ~x == -(x + 1)
    #nq  = Member.query.filter(~Member.username.in_(['andrew','michelle'])).all()
    #
    #print(nq)
    #
    ##robot = Member(username='robot',password='$y$asdasd')
    ##db.session.add(robot)
    ##db.session.commit()
    
    #qnull = Member.query.filter(Member.email == None).all()
    #print('\n', qnull)
    
    #and
    #q = Member.query.filter(Member.username == 'andrew').filter(Member.email == 'andrew@msn.com').all()
    #print(q)
    #
    #qbad = Member.query.filter(Member.username == 'andrew').filter(Member.email == 'andrew@msn').all()
    #print(qbad)
    #
    #q2 = Member.query.filter(db.and_(Member.username == 'andrew',Member.email == 'andrew@msn.com')).all()
    #print(q2)
    
    #or
    #q = Member.query.filter(db.or_(Member.username == 'andrew',Member.email == 'keanu@aol.com')).all()
    #print(q)    
    #
    #q2 = Member.query.filter(db.or_(Member.username == 'andrew',Member.email == None)).all()
    #print(q2)    
    
    #order by
    #q = Member.query.all()
    #print(q)
    #q2 = Member.query.order_by(Member.username).all()
    #print("\n",q2,"\n")
    #
    #q3 = Member.query.filter(db.or_(Member.username == 'andrew',Member.username == 'dani'))
    #print(q3.all())    
    #
    #q3order = q3.order_by(Member.username)
    #print(q3order.all())
    
    ##limit (**after order_by**)
    #q = Member.query.order_by(Member.username)
    #print(q.all())
    #print('\n'*3)
    #print(q.limit(2).all())
    
    ##offset (**after order_by**)
    #q = Member.query.order_by(Member.username).limit(3)
    #print(q.all())
    #print('\n'*3)
    #q = Member.query.order_by(Member.username).offset(1).limit(3) #offset(1) is skipping the first record
    #print(q.all())
    
    ##count
    #q = Member.query.all()
    #print(q)
    #print('\n'*3)
    #q2 = Member.query.count()
    #print(q2)
    
    ##inequality
    #q = Member.query.filter(Member.id > 3).all()
    #print(q)
    #print('\n'*3)
    #
    #q1 = Member.query.filter(Member.id >= 5).all()
    #print(q1)
    #print('\n'*3)
    #
    #q2 = Member.query.filter(Member.email < 'd').all()
    #print(q2)
    
    ##one to many queries
    #andrew = Member.query.filter(Member.username == 'andrew').first()
    #print(andrew.id)
    #print('\n'*3)
    #
    #order = Orders(price=55,member_id=andrew.id)
    ##creating the order using the virtual sqlalchemy column
    #order2 = Orders(price=200,member=andrew)
    #db.session.add(order)
    #db.session.add(order2)
    #db.session.commit()
    #
    #print(andrew.orders.all())
    
    #many to many queries
    #course1 = Course(name='Course One')
    #course2 = Course(name='Course Two')
    #course3 = Course(name='Course Three')
    #course4 = Course(name='Course Four')
    #course5 = Course(name='Course Five')
    #db.session.add(course1)
    #db.session.add(course2)
    #db.session.add(course3)
    #db.session.add(course4)
    #db.session.add(course5)
    #db.session.commit()
    
    #andrew = Member.query.filter(Member.username == 'andrew').first()
    #michelle = Member.query.filter(Member.username == 'michelle').first()
    #
    #course1 = Course.query.filter(Course.name == 'Course One').first()
    #course2 = Course.query.filter(Course.name == 'Course Two').first()
    #
    #print(course1.member)
    #
    ##course1.member.append(andrew)
    ##course1.member.append(michelle)
    #course2.member.append(andrew)
    #db.session.commit()
    ##using backref
    #print(course1.member)
    #
    #print(andrew.courses.all())
    
    