import SwiftUI
import FirebaseDatabase

//struct LogView: View {
//    @ObservedObject var viewModel = ReadViewModel()
//    @State private var selectedQuestion: String?
//
//    var body: some View {
//        List {
//            ForEach(viewModel.entries.sorted(by: { $0.date > $1.date }), id: \.date) { entry in
//                Section(header: Text(entry.date)) {
//                    ForEach(entry.prompts, id: \.question) { prompt in
//                        DisclosureGroup(prompt.question) {
//                            Text(prompt.answer)
//                        }
//                    }
//                }
//            }
//        }
//        .onAppear {
//            viewModel.readDataFromDatabase(uid: "TqbRkGwH6eQ7kqq85WV1Hemm7bQ2", date: "2023-10-13") { jsonData in
//                // Process jsonData to populate viewModel.entries
//            }
//        }
//    }
//}


// Define a SwiftUI View
struct LogView: View {
    @ObservedObject var viewModel = ReadViewModel()
    
    var body: some View {
        Text("Check console for printed data")
            .onAppear {
                viewModel.readDataFromDatabase(uid: "TqbRkGwH6eQ7kqq85WV1Hemm7bQ3", date: "2023-10-14") { jsonData in
                    // This closure will be executed once data is fetched
                }
            }
    }
}

//struct Entry: Identifiable {
//    var id = UUID()
//    var date: String
//    var prompts: [Prompt]
//}
//
//struct Prompt: Identifiable {
//    var id = UUID()
//    var question: String
//    var answer: String
//}

class ReadViewModel: ObservableObject {
//    @Published var entries: [Entry] = []

    private let ref = Database.database().reference()

    func readDataFromDatabase(uid: String, date: String, completion: @escaping ([String: Any]) -> Void) {
        let dailyEntriesRef = ref.child("users").child(uid).child("dailyEntries").child(date)
        
//        dailyEntriesRef.observeSingleEvent(of: .value) { snapshot, error in
//            guard error == nil, let value = snapshot.value as? [String: Any] else {
//                completion([:])
//                return
//            }
//            completion(value)
//        }
//        
        dailyEntriesRef.observeSingleEvent(of: .value) { snapshot, error in
            if let error = error {
                print("Error reading data: \(error)")
                completion([:])
                return
            }
            print("reached this point")
            guard let value = snapshot.value as? [String: Any] else {
                print("Data is not in the expected format.")
                completion([:])
                return
            }
            
            print("Fetched data: \(value)")
            completion(value)
        }
    }
    
    

}

//struct LogView_Previews: PreviewProvider {
//    static var previews: some View {
//        LogView()
//    }
//}


// Preview Provider for LogView
struct LogView_Previews: PreviewProvider {
    static var previews: some View {
        LogView()
    }
}

#Preview {
    LogView()
}
