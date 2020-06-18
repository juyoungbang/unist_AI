(define (domain deliver)
    (:types CUSTOMER STORE FOOD TRUNK)

    (:predicates 
        (customer ?c)
        (store ?s)
        (food ?f)
        (space ?t)

        (loaded ?t)
        (obj-at ?o1 ?o2)
        (driver-at ?location)
        (order ?c ?s)
        (order-done ?c)        
    )
                  
    (:functions 
        (total-cost)
        (distance ?from ?to)
    )

    (:action pick-up
        :parameters (?f ?s ?t)
        :precondition (and
            (space ?t)
            (not (loaded ?t))

            (store ?s)
            (driver-at ?s)
            (obj-at ?f ?s)
        )
        :effect (and 
            (not (obj-at ?f ?s))
            (obj-at ?f ?t)
            (loaded ?t)
        )
    )

    (:action deliver 
        :parameters (?f ?c ?t)
        :precondition (and
            (space ?t)
            (loaded ?t)

            (customer ?c)
            (driver-at ?c)

            (obj-at ?f ?t)
            (order ?f ?c)
        )
        :effect (and
            (not (obj-at ?f ?t))
            (not (loaded ?t))

            (obj-at ?f ?c)
            (order-done ?f)
        )      
    )

    (:action move 
        :parameters (?from ?to)
        :precondition (and 
            (driver-at ?from) 
            (or (customer ?to) 
                (store ?to) 
            )
        )
        :effect (and
            (increase (total-cost) (distance ?from ?to))
            (not (driver-at ?from))
            (driver-at ?to)
        )
    )
)

