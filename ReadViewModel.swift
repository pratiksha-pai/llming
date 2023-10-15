import Foundation
import FirebaseDatabase
import FirebaseDatabaseSwift

class ReadViewModel: ObservableObject{
    
    private let ref = Database.database().reference()
    
    
    func readDataFromDatabase(uid: String, date: String, completion: @escaping ([String: [String: String]]) -> Void) {
        // Reference to the "dailyEntries" node for the specified user and date
        let dailyEntriesRef = Database.database().reference().child("users").child(uid).child("dailyEntries").child(date)
        
        dailyEntriesRef.observeSingleEvent(of: .value) { snapshot, error in
            if let error = error {
                print("Error reading data from the database: \(error)")
                completion([:])
                return
            }
            
            if let entriesDict = snapshot.value as? [String: [String: String]] {
                completion(entriesDict)
            } else {
                completion([:])
            }
        }
    }

}