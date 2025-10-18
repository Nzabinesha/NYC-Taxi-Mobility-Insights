FUNCTION top_k_trips(trips, K):
    top_list = []                         # Initialize empty list to store top K trips

    FOR each trip IN trips:                # Loop through all trip records
        inserted = FALSE                   # Flag to check if trip is added to top_list

        FOR i FROM 0 TO length(top_list)-1:
            IF trip.distance > top_list[i].distance:
                INSERT trip AT position i IN top_list
                inserted = TRUE
                BREAK

        IF inserted == FALSE AND length(top_list) < K:
            APPEND trip TO top_list       # Add trip if list has fewer than K items

        IF length(top_list) > K:
            REMOVE last element           # Keep list size at K

    RETURN top_list                        # Return top K trips
