# ASP
>Any good way to indicate who is working on what to avoid concurrency?


TO-DO: (arranged by importance)
- [ ] Registration
  - create new model for Registration information
  - view function for handling the registration given the token(link)
  - html template
- [ ] Authentication
  - view function for login page(with corresponding routing)
  - html template
- [ ] Warehouse Order Processing (see the original prototype for a rough idea)
  - [ ] create new model for Warehouse Personnel
  - [ ] view function for: view the priority queue
    - routing
    - html template
  - [ ] view function for: remove order from the top of the queue(status changes from Queued for Processing to Processing by Warehouse)
    - routing in and out
    - html template
  - [ ] view function for: view details of the order removed
    - routing
    - html template
  - [ ] view function for: obtain shipping label in PDF
    - routing
    - generate PDF(as http response?)
  - [ ] view function for: update order status(status changes from Processing by Warehouse to Queued for Processing)
- [ ] Clinic manager: View Orders
  - view function for: view the placed orders
    - routing
    - html template
  - view function for: cancel order
  - view function for: update order status from Dispatched to Delivered
- [ ] Clinic manager: Checkout
  - modify the view function to:
    - display total weight of the current order
    - perform weight limit check: total weight + 1.2kg < 25
    - allow clinic manager to remove items in current order or adjust quantity
    - multiple same items should be displayed as one
- [ ] Add image field in Supply and link image files in html
- [ ] Include supply description wherever it should be
- [ ] modify the getRoute function to cater for tiebreak
- [ ] Modify project structure (make it more modular, divide fuctionalities into apps)
- [ ] email system
