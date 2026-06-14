import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# ─────────────────────────────────────────
# 17 OBJECT-ORIENTED PROGRAMMING TOPICS
# ─────────────────────────────────────────
topics = [
    {
        "id": "oop-class-obj",
        "num": "01",
        "chapter": "OOP Fundamentals",
        "title": "Class & Object",
        "subtitle": "The foundational blueprint and instance paradigms of OOP.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Core Definition</div>
  <p><strong>Class:</strong> A user-defined data type acting as a blueprint. Occupies no memory at runtime. Stores method templates and member definitions.</p>
  <p><strong>Object:</strong> A basic runtime entity. An instance of a class. Occupies physical memory space on the heap or stack.</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; line-height:1.3; background:white; border:1px solid #CBD5E0; padding:10px; border-radius:6px; width:100%;">
  <strong>Class blueprint definition:</strong><br>
  class Car { String model; int year; }<br><br>
  <strong>Object instantiation (RAM):</strong><br>
  Car myCar = new Car("Tesla", 2024);<br>
  (Allocates memory for 'model' and 'year')
</div>
<div class="box box-industry">
  <div class="box-title">JVM Heap vs Stack memory allocation</div>
  <p><strong>Stack:</strong> Stores reference variables (e.g. <code>myCar</code>) and local variables. Deallocated automatically when methods exit.<br>
  <strong>Heap:</strong> Stores actual objects (e.g. <code>new Car()</code>) dynamically. Subject to Garbage Collection when unreferenced.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Does a Class occupy memory space? How does it differ from an Object in memory?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Logical Blueprint</span>
    <span class="buzz-tag">Physical Entity</span>
    <span class="buzz-tag">Instance Creation</span>
    <span class="buzz-tag">Heap Allocation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"No, a Class is a logical template that does not occupy physical RAM. Memory is allocated only when an Object (an instance of the class) is created. The object's member variables are loaded into the heap or stack at execution time."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is an anonymous object?"</p>
  <p class="followup-a">An object created without a reference variable (e.g. `new Car().drive();`). It is immediate garbage collected after the statement executes.</p>
</div>
""",
        "trap": "Don't say static variables belong to the object. Static variables are shared at the class level and exist in global memory, not inside the object's instance space.",
        "trick": "Class = Architectural blueprint. Object = The actual physical house built from the blueprint."
    },
    {
        "id": "oop-const-dest",
        "num": "02",
        "chapter": "OOP Fundamentals",
        "title": "Constructor & Destructor",
        "subtitle": "Initializing state during allocation and reclaiming resources during deallocation.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Lifecycle Methods</div>
  <p><strong>Constructor:</strong> Special member function called automatically when an object is created. Has same name as class, no return type. Can be default, parameterized, or copy constructor.</p>
  <p><strong>Destructor:</strong> Called automatically when an object goes out of scope or is deleted. Cleans up memory, files, or database locks. Preceded by tilde (~) in C++.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; line-height:1.25; background:white; border:1px solid #CBD5E0; padding:8px; border-radius:6px; width:100%; text-align:left;">
    <strong>Constructor Chaining Execution Order:</strong><br>
    1. Parent static blocks<br>
    2. Child static blocks<br>
    3. Parent instance initializers &amp; Constructor<br>
    4. Child instance initializers &amp; Constructor
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Constructor Delegation (C++11/Java)</div>
  <p>Allows a constructor to call another constructor in the same class (using <code>this()</code> in Java or initializer lists in C++) to prevent duplicate initialization code.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Can a Constructor be private? What happens if you define a private constructor?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Singleton Design</span>
    <span class="buzz-tag">Instance Prevention</span>
    <span class="buzz-tag">Factory Method</span>
    <span class="buzz-tag">Static Builder</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Yes, a constructor can be private. This prevents external code from instantiating the class using `new`. It is commonly used in the **Singleton Design Pattern** or utility classes, where access to the single instance is controlled via a static factory method."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Does Java support destructors?"</p>
  <p class="followup-a">No. Java manages memory automatically using a garbage collector. C++ requires explicit destructors to free heap allocations and prevent memory leaks.</p>
</div>
""",
        "trap": "Don't forget that if you define a parameterized constructor, the compiler stops generating the default no-argument constructor automatically.",
        "trick": "Constructor = Birth certificate setup. Destructor = Will execution and property cleanup."
    },
    {
        "id": "oop-inheritance",
        "num": "03",
        "chapter": "The Four Pillars",
        "title": "Pillar 1: Inheritance",
        "subtitle": "Creating hierarchical relationships to reuse class code structures.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Code Reuse</div>
  <p>Allows a child class (subclass) to inherit fields and methods from a parent class (superclass), establishing an **IS-A** relationship.</p>
  <p style="margin-top:6px; font-weight:800; color:#EA763F;">Types of Inheritance:</p>
  <p>Single, Multiple (interfaces in Java), Multi-level, Hierarchical, Hybrid.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%; text-align:center;">
    <strong>The Diamond Problem (Multiple Inheritance)</strong><br>
    Class A (defines <code>show()</code>)<br>
    ↙ &nbsp; &nbsp; &nbsp; &nbsp; ↘<br>
    Class B &nbsp; &nbsp; &nbsp; &nbsp; Class C (both override <code>show()</code>)<br>
    ↘ &nbsp; &nbsp; &nbsp; &nbsp; ↙<br>
    <strong>Class D</strong> (Which <code>show()</code> does it run? Compiler error!)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Upcasting vs Downcasting safety</div>
  <p><strong>Upcasting:</strong> Casting child to parent (e.g. <code>Animal a = new Dog();</code>). Safe and implicit.<br>
  <strong>Downcasting:</strong> Casting parent to child (e.g. <code>Dog d = (Dog) a;</code>). Unsafe; throws <code>ClassCastException</code> unless verified using <code>instanceof</code>.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does Java block multiple inheritance of classes, and how does it resolve the Diamond Problem?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Diamond Problem</span>
    <span class="buzz-tag">Ambiguity Resolution</span>
    <span class="buzz-tag">Interface Default</span>
    <span class="buzz-tag">Method Signature</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Java blocks multiple inheritance of classes to prevent compiler ambiguity (the Diamond Problem). If two parents define the same method, the child doesn't know which to execute. Java resolves this by supporting multiple inheritance only through **Interfaces**, where the child must explicitly override conflicting default methods."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between IS-A and HAS-A?"</p>
  <p class="followup-a">IS-A represents inheritance (e.g. Dog is an Animal). HAS-A represents composition/association (e.g. Dog has a Collar reference).</p>
</div>
""",
        "trap": "Don't state that interfaces in Java have no implementation code anymore. Java 8 introduced `default` and `static` methods that can have active code blocks.",
        "trick": "Inheritance is like inheriting your parents' house (ready to use), while interfaces are architectural guidelines you must construct yourself."
    },
    {
        "id": "oop-polymorphism",
        "num": "04",
        "chapter": "The Four Pillars",
        "title": "Pillar 2: Polymorphism",
        "subtitle": "Processing objects differently based on their data type or class.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Behavioral Adaption</div>
  <p>Polymorphism means 'many forms'. It allows a single interface or method signature to act differently depending on the context.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Type</th>
        <th>Binding Stage</th>
        <th>Mechanism</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Compile-Time</td><td>Static (Compile)</td><td>Method Overloading</td></tr>
      <tr><td>Run-Time</td><td>Dynamic (Execution)</td><td>Method Overriding</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Dynamic Method Dispatch Mechanics</div>
  <p>When an overridden method is called, the runtime checks the actual object type in memory. The CPU resolves the call using a method reference array (VTABLE). This dereference step is why overriding adds a tiny performance penalty compared to static overloading.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain Run-Time Polymorphism. How does the JVM determine which method to execute at runtime?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Upcasting</span>
    <span class="buzz-tag">Dynamic Method Disp</span>
    <span class="buzz-tag">Override Lookup</span>
    <span class="buzz-tag">VTABLE Reference</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Run-time polymorphism (Dynamic Method Dispatch) occurs when a parent reference points to a child object. At compile time, the compiler checks the parent reference type. At runtime, the JVM looks up the actual object's type on the heap and executes its overridden method."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Can static methods be overridden?"</p>
  <p class="followup-a">No. Static methods belong to the class, not instance. Attempting to override a static method results in **Method Hiding**, resolved at compile time.</p>
</div>
""",
        "trap": "Don't confuse overloading with overriding. Overloading uses different signatures in the same class. Overriding uses identical signatures in child classes.",
        "trick": "Overloading = same tool, different attachments. Overriding = same button, different actions on child devices."
    },
    {
        "id": "oop-abstraction",
        "num": "05",
        "chapter": "The Four Pillars",
        "title": "Pillar 3: Abstraction",
        "subtitle": "Hiding implementation details, showing only essential properties.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Complexity Control</div>
  <p>Abstraction focuses on **what** an object does rather than **how** it does it, reducing design complexity. Implemented using Abstract Classes and Interfaces.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; text-align:center; border:1px solid #CBD5E0; padding:6px; background:white; width:100%;">
    <strong>Abstraction Levels:</strong><br>
    Concrete Class (0%) &rarr; Abstract Class (0-100%) &rarr; Interface (100% Pure Abstraction)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Interface Contracts in Architecture</div>
  <p>Interfaces decouple modules. By programming to an interface (e.g. <code>List</code> rather than <code>ArrayList</code>), you can swap implementations without breaking application modules.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does Abstraction differ from Encapsulation? Aren't they both hiding data?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Design Level Hide</span>
    <span class="buzz-tag">Implementation Level</span>
    <span class="buzz-tag">Data Wrapping</span>
    <span class="buzz-tag">Complexity Reduction</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Abstraction hides implementation details at the **design level** to focus on interface behaviors. Encapsulation hides data variables at the **implementation level** by wrapping variables and methods into a single class, protecting state from unauthorized modification."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a concrete class?"</p>
  <p class="followup-a">A standard class that implements all its methods and can be directly instantiated (unlike abstract classes or interfaces).</p>
</div>
""",
        "trap": "Don't say abstract classes are identical to interfaces. Abstract classes can hold private state variables and concrete constructors; interfaces are strictly design contracts.",
        "trick": "Abstraction = The dashboard interface. Encapsulation = The locked hood protecting the engine parts."
    },
    {
        "id": "oop-encapsulation",
        "num": "06",
        "chapter": "The Four Pillars",
        "title": "Pillar 4: Encapsulation",
        "subtitle": "Wrapping data variables and methods into a single protective unit.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Data Protection</div>
  <p>Prevents direct access to data fields from outside the class boundary. Member variables are marked **private**, and accessed only through **public getter/setter methods**.</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; border:1px solid #CBD5E0; padding:10px; background:white; border-radius:6px; width:100%;">
  <strong>Encapsulated Class Wrapper</strong><br>
  class BankAccount {<br>
  &nbsp;&nbsp;<strong>private</strong> double balance;<br>
  &nbsp;&nbsp;<strong>public</strong> void deposit(double val) {<br>
  &nbsp;&nbsp;&nbsp;&nbsp;if (val > 0) balance += val; // validation check<br>
  &nbsp;&nbsp;}<br>
  }
</div>
<div class="box box-industry">
  <div class="box-title">Thread Safety via Encapsulation</div>
  <p>By hiding fields behind private modifiers, we prevent concurrent threads from modifying class state directly. We can add synchronization locks inside getter/setter methods to enforce thread-safety rules.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the benefit of using Getter/Setter methods instead of making class variables public?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Data Validation</span>
    <span class="buzz-tag">ReadOnly Property</span>
    <span class="buzz-tag">Access Restriction</span>
    <span class="buzz-tag">State Guarding</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Public getters/setters let us control data entry through validation rules, preventing invalid states (e.g. setting age to -5). They also allow making variables read-only by omitting setters, protecting the class's internal state."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Is encapsulation broken if a getter returns a mutable object reference?"</p>
  <p class="followup-a">Yes. Returning direct references to mutable objects allows external code to modify class state. Getters should return deep copies instead.</p>
</div>
""",
        "trap": "Don't confuse encapsulation with security encryption. Encapsulation is a design pattern for structure control, not cryptographic protection.",
        "trick": "Encapsulation is like a medical capsule: it wraps the ingredients to protect them from external elements."
    },
    {
        "id": "oop-overload-override",
        "num": "07",
        "chapter": "Method Operations",
        "title": "Overloading vs Overriding",
        "subtitle": "Different method signatures in one class vs matching signatures in subclasses.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Behavior Mapping</div>
  <p><strong>Overloading:</strong> Multiple methods in the same class share a name but have different parameter counts or types. Return type changes alone are not allowed.</p>
  <p><strong>Overriding:</strong> A subclass redefines a method from its parent class using the exact same signature (name, parameter list, and return type).</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.2pt;">
    <thead>
      <tr><th>Property</th><th>Overloading</th><th>Overriding</th></tr>
    </thead>
    <tbody>
      <tr><td>Scope</td><td>Same class</td><td>Child subclasses</td></tr>
      <tr><td>Arguments</td><td>Must change</td><td>Must match exactly</td></tr>
      <tr><td>Return Type</td><td>Can differ</td><td>Must be covariant</td></tr>
      <tr><td>Access Level</td><td>Any</td><td>Must not restrict</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Covariant Return Types</div>
  <p>During overriding, a child subclass method is allowed to return a subtype of the return type declared in the parent class (e.g., parent returns <code>Shape</code>, child returns <code>Circle</code>).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why can't you overload a method in Java by changing ONLY the return type?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Signature Ambiguity</span>
    <span class="buzz-tag">Call Resolution</span>
    <span class="buzz-tag">Return Type Excl.</span>
    <span class="buzz-tag">Compiler Error</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Because call resolution is based on parameters, not return values. If you call a method `calculate()` without assigning the result, the compiler cannot resolve which version to run based on return type alone, causing a compile error."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a covariant return type in overriding?"</p>
  <p class="followup-a">An overriding method in a subclass is allowed to return a subtype of the class returned by the parent method (e.g. parent returns Shape, child returns Circle).</p>
</div>
""",
        "trap": "Don't forget: Overriding methods cannot throw broader checked exceptions than the parent method, nor can they reduce access permissions (e.g. public cannot become private).",
        "trick": "Overload = Same method name, different input parameters. Override = Child rewriting parent rules."
    },
    {
        "id": "oop-vtable",
        "num": "08",
        "chapter": "Method Operations",
        "title": "Virtual Function & VTABLE",
        "subtitle": "Analyzing C++ dynamic dispatch using virtual method tables.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Dynamic Dispatch</div>
  <p>C++ uses a **Virtual Table (VTABLE)** to resolve function addresses at runtime during dynamic dispatch.</p>
  <p>If a class defines a virtual function: the compiler inserts a hidden pointer (<code>_vptr</code>) pointing to the class's static VTABLE containing method pointers.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%;">
    <strong style="color:#C53030; display:block; text-align:center; margin-bottom:4px;">VTABLE Lookup Flow</strong>
    <p style="font-size:7pt; color:#4A5568; line-height:1.35; text-align:center;">
      Object Instance (contains <code>_vptr</code>)<br>
      ↓ points to<br>
      Class VTABLE [MethodA *ptr, MethodB *ptr]<br>
      ↓ executes<br>
      Heap memory target function address
    </p>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Virtual Destructors Importance</div>
  <p>If a parent class base pointer deletes a child class instance, and the parent destructor is not declared <code>virtual</code>, only the parent destructor runs. The child's destructor is bypassed, causing memory leaks.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain how a VTABLE resolves dynamic dispatch at runtime for a child class overriding parent methods."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">vptr Offset</span>
    <span class="buzz-tag">Static Array Ptr</span>
    <span class="buzz-tag">Dynamic Binding</span>
    <span class="buzz-tag">Object Overhead</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"When a class defines a virtual function, the compiler inserts a hidden `_vptr` into the object. At runtime, when calling `base->draw()`, the CPU reads `_vptr` to find the class's VTABLE, reads the method pointer at the correct offset, and jumps to that address, executing the child's override."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why do we need virtual destructors?"</p>
  <p class="followup-a">If a base pointer deleting a child class lacks a virtual destructor, only the base destructor runs, failing to free child-specific allocations and causing memory leaks.</p>
</div>
""",
        "trap": "Don't say virtual functions have zero overhead. Reading `_vptr` and dereferencing the VTABLE adds a small delay and increases object size by 8 bytes (for the pointer).",
        "trick": "VTABLE is a directory of function pointers matching class methods to physical RAM code addresses."
    },
    {
        "id": "oop-abstract-interface",
        "num": "09",
        "chapter": "Abstract Contracts",
        "title": "Abstract Class vs Interface",
        "subtitle": "Choosing partial implementations vs strict behavioral contracts.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Structural Contracts</div>
  <p><strong>Abstract Class:</strong> Represents a partial template. Can hold state variables, private fields, and constructors. Supports single inheritance only.</p>
  <p><strong>Interface:</strong> Represents a strict behavioral contract. Variables are static constants. Supports multiple implementation links.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7pt;">
    <thead>
      <tr>
        <th>Feature</th>
        <th>Abstract Class</th>
        <th>Interface</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Multiple Inher.</td><td>No (Single Base)</td><td>Yes (Multiple Impl)</td></tr>
      <tr><td>Variables</td><td>Any access modifier</td><td>Must be static final</td></tr>
      <tr><td>Constructors</td><td>Yes</td><td>No</td></tr>
      <tr><td>Speed</td><td>Fast (Direct call)</td><td>Slower (Interface lookup)</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Marker Interfaces (Signal Flags)</div>
  <p>Marker interfaces have zero methods (e.g. <code>Cloneable</code>, <code>Serializable</code>). They act as a type flag, informing the runtime engine that the class supports specific behaviors or VM optimizations.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"When would you choose an Abstract Class over an Interface in application architecture?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Code Sharing</span>
    <span class="buzz-tag">State Variables</span>
    <span class="buzz-tag">Interface Segreg.</span>
    <span class="buzz-tag">Tight Coupling</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Choose an abstract class when subclasses share common implementation code and state variables (e.g. BaseDatabaseConnector). Choose an interface to define a decoupled behavior contract implemented by unrelated classes (e.g. Serializable)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a marker interface?"</p>
  <p class="followup-a">An empty interface with no methods (e.g. `Cloneable` in Java) used to signal metadata flags to the runtime engine.</p>
</div>
""",
        "trap": "Don't say interfaces cannot have any code in Java anymore; since Java 8, they support `default` and `static` methods.",
        "trick": "Abstract class is parent-child relationship (hereditary). Interface is a certification badge (anyone can apply and pass)."
    },
    {
        "id": "oop-associations",
        "num": "10",
        "chapter": "Object Relationships",
        "title": "Aggregation & Composition",
        "subtitle": "Distinguishing weak references from parent-owned lifecycles.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Relationship Levels</div>
  <p><strong>Association:</strong> General link between objects (e.g. Teacher and Student). Can be one-to-one or one-to-many.</p>
  <p><strong>Aggregation:</strong> Weak HAS-A link. Objects exist independently; parent deletion does not destroy the child (e.g. Department and Professor).</p>
  <p><strong>Composition:</strong> Strong HAS-A link. Parent owns child lifecycle; deleting the parent automatically destroys the child (e.g. House and Room).</p>
</div>
<div class="concept-visual">
  <div style="font-size:7.5pt; text-align:left; line-height:1.3; width:100%; border:1px solid #CBD5E0; border-radius:6px; padding:8px; background:white;">
    <strong>UML Associations Symbols:</strong><br>
    • <strong>Aggregation:</strong> Parent &lt;&gt;── Child (Empty Diamond)<br>
    • <strong>Composition:</strong> Parent ◆── Child (Filled Diamond)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Favors Composition over Inheritance</div>
  <p>Inheritance creates tight compile-time coupling (white-box reuse). Composition creates loose coupling by combining objects at runtime (black-box reuse), allowing dynamic swapping of nested references.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does Composition differ from Aggregation in code structure and lifecycle dependency?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Lifecycle Ownership</span>
    <span class="buzz-tag">Weak Association</span>
    <span class="buzz-tag">Object Destruction</span>
    <span class="buzz-tag">Nested Instantiation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In Aggregation, the child object is created outside the parent and passed in, existing independently. In Composition, the child is created inside the parent, meaning its lifecycle is tied to the parent's: deleting the parent destroys the child."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why is Composition preferred over Inheritance?"</p>
  <p class="followup-a">Composition keeps classes loosely coupled, allowing behaviors to be changed dynamically at runtime by swapping nested references, avoiding rigid inheritance trees.</p>
</div>
""",
        "trap": "Don't confuse the two. If children can exist without the parent, it is Aggregation. If not, it is Composition.",
        "trick": "Aggregation = Cars in a parking lot (lot closes, cars drive away). Composition = Engine inside a car (crashing the car destroys the engine)."
    },
    {
        "id": "oop-solid-1",
        "num": "11",
        "chapter": "SOLID Principles",
        "title": "SOLID: S & O Principles",
        "subtitle": "Single Responsibility and Open-Closed design paradigms.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Core Definitions</div>
  <p><strong>Single Responsibility Principle (SRP):</strong> A class should have only one reason to change. Reduces coupling and code drift.</p>
  <p><strong>Open-Closed Principle (OCP):</strong> Software entities should be open for extension but closed for modification. Avoids breaking existing tests.</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; padding:8px; background:white; border:1px solid #CBD5E0; border-radius:6px;">
  <strong>OCP Violation:</strong><br>
  if (shape == "Circle") drawCircle();<br>
  else if (shape == "Square") drawSquare();<br><br>
  <strong>Fix:</strong> Create abstract class Shape, override <code>draw()</code> in child classes.
</div>
<div class="box box-industry">
  <div class="box-title">SRP Violation: God Classes</div>
  <p>A class violates SRP if it has multiple reasons to change. For example, a <code>UserManager</code> class that handles user DB actions, sends verification emails, AND logs error files is a God Class that should be split.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the Open-Closed Principle (OCP). How do you extend a class's behavior without modifying its source code?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Polymorphic Abstr.</span>
    <span class="buzz-tag">Switch Case Smell</span>
    <span class="buzz-tag">Code Regressions</span>
    <span class="buzz-tag">Inheritance Extension</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"OCP states we should extend behavior using polymorphism. Instead of modifying an existing class with conditional checks, we define an abstract interface. New features are added by implementing this interface in new classes, avoiding regressions in existing code."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a smell of SRP violation?"</p>
  <p class="followup-a">A 'God Class' containing thousands of lines of code handling unrelated tasks (such as managing database connections, processing business logic, AND logging errors).</p>
</div>
""",
        "trap": "Don't apply SRP to the point of creating thousands of tiny classes with single functions; balance modularity with design readability.",
        "trick": "SRP = One tool, one job. OCP = Adding new USB attachments instead of opening the computer to solder components."
    },
    {
        "id": "oop-solid-2",
        "num": "12",
        "chapter": "SOLID Principles",
        "title": "SOLID: L, I, & D Principles",
        "subtitle": "Liskov Substitution, Interface Segregation, and Dependency Inversion.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Pillar Definitions</div>
  <p><strong>Liskov Substitution (LSP):</strong> Subtypes must be substitutable for their base types without breaking application logic.</p>
  <p><strong>Interface Segregation (ISP):</strong> Clients shouldn't be forced to depend on methods they don't use (use small, specific interfaces).</p>
  <p><strong>Dependency Inversion (DIP):</strong> Depend on abstractions, not concrete implementations.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; line-height:1.25; background:white; border:1px solid #CBD5E0; padding:8px; border-radius:6px; width:100%; text-align:left;">
    <strong>Dependency Inversion Flow:</strong><br>
    [High-Level Module] &rarr; [Interface Contract] &larr; [Low-Level Class]<br>
    (Both depend on abstraction, decoupling concrete implementations)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Dependency Injection (DI)</div>
  <p>A pattern implementing DIP by passing dependent objects into a class constructor or setter, decoupling object creation from class execution logic.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the Classic Square-Rectangle LSP violation. Why does it violate Liskov Substitution?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Subtype Invariant</span>
    <span class="buzz-tag">Unexpected Side-Effect</span>
    <span class="buzz-tag">Contract Violation</span>
    <span class="buzz-tag">Abstract Separation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"If a Square inherits from Rectangle, setting the width changes the height to maintain square constraints. If a client expects a Rectangle and sets width/height independently, they get unexpected behavior. This violates LSP because the subtype breaks the parent class's invariants."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How does Dependency Injection (DI) relate to DIP?"</p>
  <p class="followup-a">DIP is the design goal (depending on abstractions). DI is the mechanism to achieve it (injecting concrete dependencies at runtime via constructor parameters).</p>
</div>
""",
        "trap": "Don't confuse LSP with simple overriding compile checks. LSP is a behavioral contract; if subclass overrides break parent assumptions, LSP is violated.",
        "trick": "LSP = Duck test (if it looks like a duck but needs batteries, it is not a true subtype)."
    },
    {
        "id": "oop-access-mods",
        "num": "13",
        "chapter": "Language Specifics",
        "title": "Access Modifiers",
        "subtitle": "Regulating class visibility boundaries.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Visibility Levels</div>
  <p>Access modifiers define visibility scopes for classes, variables, and methods.</p>
  <p><strong>Private:</strong> Accessible only within the declaring class.</p>
  <p><strong>Default (Package-Private):</strong> Accessible within the same folder/package. No keyword.</p>
  <p><strong>Protected:</strong> Accessible within the same package + subclasses in different packages.</p>
  <p><strong>Public:</strong> Accessible globally.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.2pt;">
    <thead>
      <tr><th>Modifier</th><th>Class</th><th>Package</th><th>Subclass</th><th>Global</th></tr>
    </thead>
    <tbody>
      <tr><td>private</td><td>Yes</td><td>No</td><td>No</td><td>No</td></tr>
      <tr><td>default</td><td>Yes</td><td>Yes</td><td>No</td><td>No</td></tr>
      <tr><td>protected</td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td></tr>
      <tr><td>public</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Why Access Control Matters</div>
  <p>Restricting visibility reduces coupling. By exposing only public API methods and hiding implementation details under private modifiers, classes can be updated safely without breaking client code.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between Protected and Default (Package-Private) access modifiers in Java?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Subclass Access</span>
    <span class="buzz-tag">Package Bound</span>
    <span class="buzz-tag">Folder Boundary</span>
    <span class="buzz-tag">Access Hierarchy</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Default access restricts visibility entirely to the declaring package. Protected access extends visibility, allowing subclasses in external packages to access the member variables, which is useful for framework design."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why can't outer classes be private?"</p>
  <p class="followup-a">An outer class marked private would be unusable by any code, rendering it obsolete. Inner nested classes, however, can be marked private.</p>
</div>
""",
        "trap": "Don't reduce access permissions when overriding a method (e.g. a protected parent method cannot be overridden as private in a child class).",
        "trick": "Private = Self. Default = Family house. Protected = Family house + distant grandchildren. Public = Public street."
    },
    {
        "id": "oop-binding",
        "num": "14",
        "chapter": "Method Operations",
        "title": "Static vs Dynamic Binding",
        "subtitle": "Resolving method calls at compile time vs runtime.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Call Resolution Stages</div>
  <p><strong>Static Binding:</strong> Method call is resolved at compile time. Used for static, private, final, or overloaded methods. Faster execution.</p>
  <p><strong>Dynamic Binding:</strong> Resolved at runtime based on the actual object's type on the heap. Used for overridden methods.</p>
</div>
<div class="concept-visual">
  <div style="font-size:7.5pt; text-align:left; line-height:1.3; width:100%; border:1px solid #CBD5E0; border-radius:6px; padding:8px; background:white;">
    <strong>Binding Resolution Timelines:</strong><br>
    • <strong>Static (Early):</strong> Source Code &rarr; [Compiler Linker] &rarr; Target Address<br>
    • <strong>Dynamic (Late):</strong> Execution Run &rarr; [VTABLE/JVM Lookup] &rarr; Target Address
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Compiler Optimization (Devirtualization)</div>
  <p>Modern Just-In-Time (JIT) compilers analyze inheritance paths. If they prove a virtual method has only one implementation, they bypass the VTABLE check entirely (inlining it) for optimal CPU execution speed.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are final, static, and private methods statically bound by the compiler?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Override Prevention</span>
    <span class="buzz-tag">Class Level binding</span>
    <span class="buzz-tag">Performance Opt.</span>
    <span class="buzz-tag">Early Binding</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Static, private, and final methods cannot be overridden by subclasses. Since there is no potential for runtime changes, the compiler resolves their addresses at compile time, bypassing runtime VTABLE lookups."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Which type of binding does overloading use?"</p>
  <p class="followup-a">Static binding. The compiler resolves overloaded method calls at compile time based on the argument signatures in the code.</p>
</div>
""",
        "trap": "Don't assume dynamic binding is slow. Modern compiler optimizations and JIT compilation make the overhead of dynamic lookup negligible in most apps.",
        "trick": "Static = resolved at the factory (compile). Dynamic = resolved on the road (execution)."
    },
    {
        "id": "oop-gc-memory",
        "num": "15",
        "chapter": "Memory & Management",
        "title": "Garbage Collection & Memory",
        "subtitle": "Automatic heap cleanup vs explicit memory deallocation.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Reclaiming Memory</div>
  <p><strong>Garbage Collection (Java/Go):</strong> A background daemon thread scans heap memory to identify and delete unreachable objects. Simplifies coding but adds pause times.</p>
  <p><strong>Explicit Management (C++):</strong> Developers must manually call `delete` to free memory allocated with `new`, or use smart pointers (unique_ptr, shared_ptr).</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; line-height:1.25; background:white; border:1px solid #CBD5E0; padding:8px; border-radius:6px; width:100%; text-align:center;">
    [GC Roots (Active Stack Threads / Statics)]<br>
    &darr; references<br>
    [Object A] &rarr; [Object B] (Reachable: Safe)<br>
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [Object C] &harr; [Object D] (Unreachable: GC Sweep)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Generational Hypothesis in JVM</div>
  <p>Most allocated objects die young. Modern JVM garbage collectors divide heap memory into three zones: **Eden** (for new objects), **Survivor** spaces, and **Tenured** (for long-lived objects), optimizing scan sweeps.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a Garbage Collector know when an object is eligible for deletion? Explain GC roots."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Reachability Analysis</span>
    <span class="buzz-tag">Reference Counting</span>
    <span class="buzz-tag">GC Root Node</span>
    <span class="buzz-tag">Mark and Sweep</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Garbage collectors trace reachability starting from 'GC Roots' (like thread stack frames or static variables). If an object cannot be reached through any reference path, it is marked unreachable and scheduled for cleanup, resolving circular reference bugs."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a memory leak in a garbage-collected language?"</p>
  <p class="followup-a">When unused objects remain referenced by active objects (like growing static collections), preventing the garbage collector from reclaiming them.</p>
</div>
""",
        "trap": "Don't say `System.gc()` forces immediate garbage collection in Java. It only suggests cleanup to the JVM; the engine decides when to run.",
        "trick": "Garbage Collection is a maid service cleaning up after you. Explicit Management is cleaning up your own dishes after every meal."
    },
    {
        "id": "oop-copying",
        "num": "16",
        "chapter": "Memory & Management",
        "title": "Shallow vs Deep Copy",
        "subtitle": "Copying references vs duplicating nested heap memory.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Duplication Mechanics</div>
  <p><strong>Shallow Copy:</strong> Copies the top-level object fields. Nested objects are not duplicated; the copy shares references with the original.</p>
  <p><strong>Deep Copy:</strong> Recursively duplicates all nested objects, creating completely independent object structures in memory.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%; text-align:center;">
    <strong>Shallow Copy Pointer Sharing</strong><br>
    Original.address ──&gt; [ RAM Address Block ]<br>
    Copy.address &nbsp; &nbsp;───&gt; [ Shared Block ] (Modifications affect both!)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">The Java Cloneable Trap</div>
  <p>The standard <code>Object.clone()</code> is a shallow copy. If a class implements <code>Cloneable</code>, it must override <code>clone()</code> and manually duplicate nested mutable references to be a true deep copy.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the risk of a Shallow Copy when an object contains references to mutable data."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Reference Sharing</span>
    <span class="buzz-tag">Side-Effect Modification</span>
    <span class="buzz-tag">Clone Contract</span>
    <span class="buzz-tag">Memory Isolation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A shallow copy duplicates only member pointers, not the target data. If the copy modifies a shared mutable object (e.g. updating a list element), it directly alters the original object's state, causing hard-to-debug side-effects."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How is a deep copy implemented in Java?"</p>
  <p class="followup-a">By implementing `Cloneable` and overriding `clone()` to manually clone all nested mutable objects, or by using serialization libraries.</p>
</div>
""",
        "trap": "Don't assume `clone()` in Java performs a deep copy by default. The default `Object.clone()` method is strictly a shallow copy.",
        "trick": "Shallow Copy = Sharing a house key. Deep Copy = Building a duplicate house with its own keys."
    },
    {
        "id": "oop-copy-constructor",
        "num": "17",
        "chapter": "Language Specifics",
        "title": "Copy Const. & Assignment",
        "subtitle": "Initializing objects vs copying state into existing objects in C++.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Duplication Mechanics</div>
  <p><strong>Copy Constructor:</strong> Initializes a new object as a copy of an existing one (e.g. `Box b2 = b1;`).</p>
  <p><strong>Copy Assignment Operator:</strong> Copies state from one object into an already initialized object (e.g. `b2 = b1;`). Requires self-assignment checks.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; line-height:1.25; background:white; border:1px solid #CBD5E0; padding:8px; border-radius:6px; width:100%; text-align:left;">
    <strong>C++ Assignment vs Initialization:</strong><br>
    Box b1;<br>
    Box b2 = b1;  // Copy Constructor (Initialization)<br>
    Box b3;<br>
    b3 = b1;      // Copy Assignment Operator (Assigned)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Rule of Five (Modern C++11)</div>
  <p>If a class manages system resources, it requires defining five operations: Destructor, Copy Constructor, Copy Assignment, Move Constructor, and Move Assignment to prevent leaks and maximize pointer speed.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does a Copy Constructor accept its parameter by reference rather than by value?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Infinite Recursion</span>
    <span class="buzz-tag">Pass by Reference</span>
    <span class="buzz-tag">Object Parameter</span>
    <span class="buzz-tag">Stack Overflow</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"If a copy constructor accepted parameters by value, passing an argument would require creating a temporary copy of the object. Creating that copy would call the copy constructor again, leading to infinite recursion and stack overflow."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the Rule of Three in C++?"</p>
  <p class="followup-a">If a class requires a custom Destructor, Copy Constructor, or Copy Assignment Operator, it almost certainly needs all three to manage resources safely.</p>
</div>
""",
        "trap": "Don't forget to check for self-assignment (e.g. `if (this == &rhs) return *this;`) in your assignment operator to prevent deleting your own resources.",
        "trick": "Copy Constructor = Birth by cloning. Assignment = Copying content onto a blank canvas."
    }
]


OOP_BOOSTERS = {
    "oop-class-obj": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that a Class is a logical blueprint defining methods and attributes, while an Object is a physical instance of that class allocated on the heap at runtime."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying classes occupy memory. Only objects occupy physical RAM (except static class definitions). <strong>Depth:</strong> Differentiate compile-time classes vs runtime objects.</p>
</div>
""",
    "oop-const-dest": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Constructors initialize object member variables, whereas destructors free resources like open files or heap memory. C++ requires virtual destructors to prevent base pointer deletion memory leaks."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking Java/Python has destructors similar to C++. They rely on automated garbage collectors. <strong>Depth:</strong> Explain constructor delegation and initialization lists.</p>
</div>
""",
    "oop-inheritance": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Inheritance enables code reuse by establishing an IS-A relationship between subclasses and superclasses. In interviews, explain how to resolve the Diamond Problem using virtual base inheritance in C++ or interfaces in Java."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing Java supports multiple class inheritance. It only supports multiple interface implementations. <strong>Depth:</strong> Contrast Single, Multiple, Hierarchical, and Hybrid inheritance.</p>
</div>
""",
    "oop-polymorphism": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain polymorphism as 'one interface, many forms.' Differentiate compile-time polymorphism (overloading evaluated by signatures) from runtime polymorphism (overriding resolved via VTABLE lookups)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying static polymorphism uses virtual tables. VTABLEs are exclusive to dynamic runtime overriding dispatch. <strong>Depth:</strong> Detail performance costs of runtime binding.</p>
</div>
""",
    "oop-abstraction": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Abstraction hides implementation details and shows only functional interfaces. Illustrate this with a steering wheel interface that hides engine mechanics from the driver."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing Abstraction (design-level design hiding) with Encapsulation (data-level hiding). <strong>Depth:</strong> Contrast abstract classes vs interfaces.</p>
</div>
""",
    "oop-encapsulation": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Encapsulation binds data variables and code methods into a single unit (class), securing class state by restricting direct access through private modifiers and public getters/setters."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing encapsulation is just wrapping variables. It is about data hiding to prevent unauthorized modifications. <strong>Depth:</strong> Access modifiers scope analysis.</p>
</div>
""",
    "oop-overload-override": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Method overloading occurs within the same class (same name, different arguments, compile-time). Method overriding occurs between parent-child classes (same name and arguments, resolved at runtime)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Changing only return types to overload a method. Overloading requires unique argument signatures; return type changes alone fail compile checks. <strong>Depth:</strong> Overloading rules.</p>
</div>
""",
    "oop-vtable": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"VTABLE is a static index of function pointers created for classes with virtual methods. Every object of such class has a invisible `_vptr` pointing to this table for dynamic dispatch resolved at runtime."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking every object has its own unique VTABLE copy. VTABLE is class-static; objects only store a pointer to it (`_vptr`). <strong>Depth:</strong> Draw vptr to VTABLE mapping.</p>
</div>
""",
    "oop-abstract-interface": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"An abstract class can contain both abstract and concrete methods with instance states. An interface is a pure contract declaring behaviors. Subclasses can implement multiple interfaces but inherit only one class."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking modern interfaces can't have method bodies. Java 8+ interfaces allow default/static methods, but they still cannot hold state. <strong>Depth:</strong> Multi-inherit resolution.</p>
</div>
""",
    "oop-associations": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Differentiate HAS-A links: Aggregation is a weak association where parts can survive without the parent. Composition is a strong link where parts are parent-owned and die with it."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Drawing them same in UML. Composition is a filled diamond; Aggregation is an empty diamond. <strong>Depth:</strong> Code implementation structures (pointers vs inner classes).</p>
</div>
""",
    "oop-solid-1": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain SRP (Single Responsibility), OCP (Open-Closed: extend without modifying existing files), and LSP (Liskov Substitution: subclasses must replace bases without breaking systems)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Violating LSP by making a Square class inherit from Rectangle (setting height changes width unexpectedly). <strong>Depth:</strong> Refactor violating designs using compositions.</p>
</div>
""",
    "oop-solid-2": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain ISP (Interface Segregation: keep interfaces small to avoid forcing dummy method overrides) and DIP (Dependency Inversion: depend on abstractions, not concrete helper classes)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing DIP with Dependency Injection (DI is just a design pattern implementing DIP). <strong>Depth:</strong> Refactor coupling issues using abstraction layers.</p>
</div>
""",
    "oop-access-mods": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Access modifiers define encapsulation scopes: private (class only), default (package only), protected (class + package + subclasses), and public (unrestricted global access)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying protected variables are visible to subclasses only. In Java, they are also visible to any class in the same package. <strong>Depth:</strong> Scope hierarchy details.</p>
</div>
""",
    "oop-binding": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Static binding resolves methods at compile-time (overloaded, private, final, static methods). Dynamic binding resolves methods at runtime based on object instance type (overridden methods)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Expecting dynamic binding for private methods. Since private methods aren't inherited, they are bound statically. <strong>Depth:</strong> Compare execution speed differences.</p>
</div>
""",
    "oop-gc-memory": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Garbage Collection frees dereferenced heap memory. Standard strategies include Reference Counting (prone to cyclic reference leaks) and Mark-and-Sweep (GC starts from root nodes)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing GC guarantees no memory leaks. Forgotten references to unused objects in static collections prevent GC collection. <strong>Depth:</strong> Memory leak examples.</p>
</div>
""",
    "oop-copying": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Shallow copying clones object references, sharing inner heap-allocated resources. Deep copying duplicates the parent object and recursively clones all nested objects on the heap."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Modifying a shallow copy, unaware it alters the original object's shared lists/objects. <strong>Depth:</strong> Explain why dynamic memory objects require deep copies.</p>
</div>
""",
    "oop-copy-constructor": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A copy constructor creates a new object using an existing object of the same class. You must pass the argument by reference (e.g. `Box(const Box& other)`) to avoid infinite recursion."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Passing by value in copy constructor definitions. Passing by value triggers a copy constructor call, leading to infinite compile-time loops. <strong>Depth:</strong> Copy constructor usage.</p>
</div>
"""
}

HIGH_YIELD_TOPICS = ["oop-polymorphism", "oop-abstract-interface", "oop-solid-1"]

# ─────────────────────────────────────────
# HELPERS FOR FOLLOW-UPS AND SPACE FILLERS
# ─────────────────────────────────────────
def get_topic_followups(tid):
    followups_dict = {
        "oop-class-obj": "• What is the difference between class and struct?<br>• What is an anonymous object?",
        "oop-const-dest": "• What is constructor delegation?<br>• Can constructors be overloaded?",
        "oop-inheritance": "• What is virtual base inheritance?<br>• Why does Java avoid multiple class inheritance?",
        "oop-polymorphism": "• Differentiate compile-time vs run-time polymorphism.<br>• What is method hiding?",
        "oop-abstraction": "• Can an abstract class implement an interface?<br>• What is a concrete class?",
        "oop-encapsulation": "• Is encapsulation broken if getters return mutable references?<br>• Explain access control levels.",
        "oop-overload-override": "• Explain covariant return types.<br>• Can static methods be overridden?",
        "oop-vtable": "• What is the overhead of a virtual pointer?<br>• Draw VTABLE lookup mechanism.",
        "oop-abstract-interface": "• What is a marker interface?<br>• Why did Java 8 introduce default methods?",
        "oop-associations": "• Contrast aggregation vs composition lifecycles.<br>• What is association vs dependency?",
        "oop-solid-1": "• What is a class cohesion metric?<br>• Give a real-world SRP violation case.",
        "oop-solid-2": "• Explain how DIP differs from DI.<br>• How does LSP relate to inheritance?",
        "oop-access-mods": "• Explain protected visibility within the same package.<br>• Can outer classes be private?",
        "oop-binding": "• Explain why static methods use static binding.<br>• What is early binding?",
        "oop-gc-memory": "• Explain mark-and-sweep vs reference counting.<br>• How do memory leaks happen in Java?",
        "oop-copying": "• Contrast shallow cloning vs deep cloning.<br>• How to implement deep cloning in Java?",
        "oop-copy-constructor": "• Explain the Rule of Three in C++.<br>• Why must copy constructor pass by reference?"
    }
    return followups_dict.get(tid, "• Compare language implementation differences.<br>• How is memory managed?")

def get_oop_space_filler(tid):
    fillers = {
        "oop-class-obj": """
<div class="box box-depth">
  <div class="box-title">📈 Memory Allocation Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Logical):</strong> Class acts as variable template blueprint.<br>
    <strong>Level 2 (Stack):</strong> Local references held in thread execution stack.<br>
    <strong>Level 3 (Heap):</strong> Instance objects created in dynamic heap space.<br>
    <strong>Level 4 (Method):</strong> Static variables and code templates loaded to Metaspace.
  </div>
</div>
""",
        "oop-const-dest": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What happens if a constructor throws an exception?"<br>
    <strong>Candidate:</strong> "The object is partially constructed. The destructor will not run automatically, which can cause memory leaks unless resources are wrapped in smart pointers or cleaned up explicitly."
  </div>
</div>
""",
        "oop-inheritance": """
<div class="box box-depth">
  <div class="box-title">📈 Inheritance Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Single and multilevel class inheritance hierarchy.<br>
    <strong>Level 2 (Conflict):</strong> Resolve the Diamond Problem using virtual keywords.<br>
    <strong>Level 3 (Contract):</strong> Leverage interfaces to implement multiple inheritances.<br>
    <strong>Level 4 (Dynamic):</strong> JVM method table resolution and super delegation.
  </div>
</div>
""",
        "oop-polymorphism": """
<div class="box box-depth">
  <div class="box-title">📈 Polymorphism Bind Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Define):</strong> Understand overloading (static) vs overriding (dynamic).<br>
    <strong>Level 2 (Static):</strong> Overloading resolved at compile time via argument signature matches.<br>
    <strong>Level 3 (Dynamic):</strong> Overriding resolved at runtime by inspecting heap object types.<br>
    <strong>Level 4 (Cost):</strong> Dereferencing VTABLE pointer adds CPU branch target cache penalties.
  </div>
</div>
""",
        "oop-abstraction": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How does Abstraction help in scale systems?"<br>
    <strong>Candidate:</strong> "By defining clean interface boundaries. If we code to interfaces, we can swap database engines or payment gateways without changing core business logic modules."
  </div>
</div>
""",
        "oop-encapsulation": """
<div class="box box-depth">
  <div class="box-title">📈 State Protection Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Scope):</strong> Declare variables private, providing getters.<br>
    <strong>Level 2 (Invariants):</strong> Validate parameter inputs inside setters.<br>
    <strong>Level 3 (Read-Only):</strong> Omit setters to implement immutable states.<br>
    <strong>Level 4 (Escape):</strong> Prevent reference escape by returning deep clones.
  </div>
</div>
""",
        "oop-overload-override": """
<div class="box box-depth">
  <div class="box-title">⚖️ Operator Overloading Contrast</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>C++ Support:</strong> Allows overloading standard operators (like + or &lt;&lt;) to enhance custom class utility.<br>
    <strong>Java Exclusion:</strong> Excludes user-level operator overloading (except + for String) to prevent compiler complexity and maintain code readability.
  </div>
</div>
""",
        "oop-vtable": """
<div class="box box-depth">
  <div class="box-title">📈 Dispatch Mechanics Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Object):</strong> Object allocation inserts a hidden <code>_vptr</code> at offset 0.<br>
    <strong>Level 2 (Table):</strong> Compiler builds a static VTABLE of pointers for the class.<br>
    <strong>Level 3 (Lookup):</strong> Target call queries <code>_vptr</code> to locate the class's VTABLE.<br>
    <strong>Level 4 (Jump):</strong> CPU reads pointer from VTABLE index and performs a jump.
  </div>
</div>
""",
        "oop-abstract-interface": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why did Java 8 introduce default interface methods?"<br>
    <strong>Candidate:</strong> "To allow adding new methods to existing interfaces without breaking all their implementing classes, enabling backward-compatible library extension."
  </div>
</div>
""",
        "oop-associations": """
<div class="box box-depth">
  <div class="box-title">📈 Relationship Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Association):</strong> Bidirectional or unidirectional links (e.g. Student-Course).<br>
    <strong>Level 2 (Aggregation):</strong> Weak link; objects exist independently (e.g. Employee-Office).<br>
    <strong>Level 3 (Composition):</strong> Strong parent ownership; nested instances (e.g. Document-Page).<br>
    <strong>Level 4 (Coupling):</strong> Composition preferred over subclassing to decouple systems.
  </div>
</div>
""",
        "oop-solid-1": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you violate OCP?"<br>
    <strong>Candidate:</strong> "By using complex switch-case or if-else trees inside a core class to handle different behaviors. Adding a behavior requires rewriting the class, risking regression bugs."
  </div>
</div>
""",
        "oop-solid-2": """
<div class="box box-depth">
  <div class="box-title">📈 SOLID Integration Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (SRP):</strong> Split classes based on actors and business responsibilities.<br>
    <strong>Level 2 (OCP):</strong> Drive interfaces to allow extension without editing core files.<br>
    <strong>Level 3 (LSP):</strong> Ensure subtypes fulfill parent contracts completely.<br>
    <strong>Level 4 (DIP):</strong> Use Dependency Injection to inject mock implementations.
  </div>
</div>
""",
        "oop-access-mods": """
<div class="box box-depth">
  <div class="box-title">⚖️ Access modifier limits</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Private:</strong> Strictly scoped to class; hidden from nested entities.<br>
    <strong>Default:</strong> Package private; allows fast communication within folders.<br>
    <strong>Protected:</strong> Safe inheritance door; lets subclass hooks extend base models.<br>
    <strong>Public:</strong> Global access; acts as the API face. Keep this as small as possible.
  </div>
</div>
""",
        "oop-binding": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Does Java use static binding for overloaded methods?"<br>
    <strong>Candidate:</strong> "Yes. The compiler evaluates the arguments of the method call at compile-time and maps it to the unique overloaded signature, resolving the call address early."
  </div>
</div>
""",
        "oop-gc-memory": """
<div class="box box-depth">
  <div class="box-title">📈 GC Algorithms Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Ref Count):</strong> Count active links; fails on circular reference loops.<br>
    <strong>Level 2 (Tracing):</strong> Scan reachable nodes starting from active GC roots.<br>
    <strong>Level 3 (Generational):</strong> Divide objects by age into Eden, Survivor, and Tenured spaces.<br>
    <strong>Level 4 (JIT/Escape):</strong> Allocate objects directly on the stack via escape analysis.
  </div>
</div>
""",
        "oop-copying": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you perform a deep copy in Java easily?"<br>
    <strong>Candidate:</strong> "We can implement a copy constructor that manually duplicates nested references, or serialize the object to JSON/bytes and deserialize it back into a new object."
  </div>
</div>
""",
        "oop-copy-constructor": """
<div class="box box-depth">
  <div class="box-title">📈 Rule of Three/Five/Zero</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Rule of Three:</strong> Custom destructor, copy constructor, and copy assignment are required together.<br>
    <strong>Rule of Five:</strong> Adds move constructor and move assignment for performance.<br>
    <strong>Rule of Zero:</strong> Use smart pointers and standard library templates to avoid manual lifecycle code.
  </div>
</div>
"""
    }
    return fillers.get(tid, get_default_space_filler())

def get_default_space_filler():
    return """
<div class="box box-depth">
  <div class="box-title">📈 Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Understand the main definition and syntax.<br>
    <strong>Level 2 (Intermediate):</strong> Learn execution trace and typical memory states.<br>
    <strong>Level 3 (Advanced):</strong> Analyze corner cases and optimization schemes.<br>
    <strong>Level 4 (Expert):</strong> Handle system integration trade-offs.
  </div>
</div>
"""

# ─────────────────────────────────────────
# DYNAMIC LAYOUT HELPERS (INDUSTRY USAGE & INTERVIEW DEPTH)
# ─────────────────────────────────────────
def get_oop_industry_box(tid):
    industry_usage = {
        "oop-class-obj": "Enterprise frameworks (like Spring or Hibernate) use class blueprints to dynamically instantiate beans and map database rows to Java objects via reflection.",
        "oop-const-dest": "Thread pools (like ExecutorService) and database connection pools (like HikariCP) use constructors to pre-allocate connections and cleanup methods to safely release sockets.",
        "oop-inheritance": "UI frameworks (like Android SDK or iOS UIKit) structure views in deep hierarchy trees (e.g. TextView inherits from View) to inherit layout characteristics.",
        "oop-polymorphism": "JDBC drivers implement interfaces (like Connection) polymorphically; the same connection code behaves differently for MySQL, PostgreSQL, or Oracle at runtime.",
        "oop-abstraction": "Cloud SDKs (like AWS S3 SDK) expose abstract interfaces (S3Client) to decouple client business logic from raw network call implementations.",
        "oop-encapsulation": "REST API request/response payloads (DTOs) encapsulate raw JSON fields using private properties and validate input formats inside getter/setter methods.",
        "oop-overload-override": "Logging libraries (like Log4j) overload method signatures to accept varying arguments (String, Exception, Object[]) for runtime logging convenience.",
        "oop-vtable": "Operating system kernels (written in C++) and high-performance game engines (like Unreal Engine) optimize virtual tables to dispatch event handlers with minimal CPU overhead.",
        "oop-abstract-interface": "Spring Security uses interfaces (UserDetailsService) for contract definition and abstract classes (WebSecurityConfigurerAdapter) to provide default configurations.",
        "oop-associations": "Domain-driven design (DDD) maps database relations using associations: composition for nested entities (Order-LineItem), aggregation for lookup items (Product-Category).",
        "oop-solid-1": "E-commerce checkouts use OCP by defining payment strategy interfaces, allowing new payment methods (Stripe, PayPal) to be added without changing the core checkout orchestrator.",
        "oop-solid-2": "Dependency injection containers (like Spring IoC or NestJS) implement DIP to inject mock repository interfaces during testing, decoupling code from database instances.",
        "oop-access-mods": "SDK library developers use package-private (default) visibility to restrict internal utility classes from being accessed by external API clients, maintaining API safety.",
        "oop-binding": "Java compiler uses static binding for overloaded helper methods (e.g. Math.max) for speed, and dynamic binding for overriding to enable runtime strategy patterns.",
        "oop-gc-memory": "Low-latency trading systems tune GC flags (like ZGC or G1GC) to minimize garbage collection stop-the-world pauses, avoiding financial transaction delays.",
        "oop-copying": "Redux in React and event sourcing systems require deep copying or immutable updates (using object spread or libraries like Immer) to prevent side-effects in application state.",
        "oop-copy-constructor": "Game engines (like Unity or Unreal Engine) copy complex game objects (e.g. cloning a prefab enemy) using copy constructors to avoid reloading texture assets from disk."
    }
    desc = industry_usage.get(tid, "Framework design patterns utilize polymorphism and interfaces to decouple consumer applications from library implementation details.")
    return f"""
<div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
  <div class="box-title" style="font-size: 8pt; color: #B7791F; margin-bottom: 4px;">🏭 Where Used in Industry</div>
  <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">{desc}</p>
</div>
"""

def get_oop_depth_box(tid):
    depth_levels = {
        "oop-class-obj": [
            "Class vs Object blueprint definition.",
            "Differences in memory allocation (Stack vs Heap).",
            "Class loader subsystem and Metaspace loading.",
            "Overhead of object headers (Mark Word, Klass Word).",
            "Object pooling pattern to avoid garbage collection."
        ],
        "oop-const-dest": [
            "Purpose of constructor and destructor lifecycle.",
            "Initialization block execution vs constructor code.",
            "Constructor chaining, virtual base construction in C++.",
            "Exceptions in constructors and resource safety (RAII).",
            "Placement of destructors in smart pointers and standard containers."
        ],
        "oop-inheritance": [
            "Code reuse using subclassing/super delegation.",
            "Overriding vs inheriting fields (no polymorphism for fields).",
            "Virtual base class pointer offsets in C++ memory layout.",
            "Tight coupling vulnerability (Fragile Base Class problem).",
            "Composition-over-inheritance design pattern implementations."
        ],
        "oop-polymorphism": [
            "Definition of overloading (static) vs overriding (dynamic).",
            "Binding stage differences: compile-time vs runtime execution.",
            "VTABLE virtual method resolution and method dispatch mechanism.",
            "Performance costs of CPU cache misses during VTABLE lookups.",
            "Polymorphic interface adapters in decoupled enterprise architectures."
        ],
        "oop-abstraction": [
            "Hiding background details using high-level declarations.",
            "Decoupled abstract interface vs detailed implementation class.",
            "Compilation firewall (Pimpl idiom in C++) to prevent rebuilds.",
            "Over-engineering risk and API evolution backward-compatibility.",
            "Exposing stable service interfaces to client microservices."
        ],
        "oop-encapsulation": [
            "Protecting state using private fields and public get/set accessors.",
            "Data hiding vs encapsulation (hiding implementation complexity).",
            "Reference escape prevention by returning defensive deep copies.",
            "Performance overhead of getter/setter boilerplate code.",
            "Enforcing domain invariants inside Domain-Driven Design aggregates."
        ],
        "oop-overload-override": [
            "Overloading (signature change) vs Overriding (behavior change).",
            "Return type rules: covariant returns in overriding methods.",
            "JVM resolution of static vs virtual method dispatch opcodes.",
            "Fragile subclassing if base class overloads are overridden.",
            "API design convenience vs maintaining code base readability."
        ],
        "oop-vtable": [
            "Dynamic binding using a hidden pointer in the object.",
            "Direct method calls vs indirect pointer dereferencing calls.",
            "Object offset 0 virtual pointer (_vptr) mapping to class VTABLE.",
            "Memory overhead of storing virtual pointer inside small objects.",
            "High-speed assembly jumps and compiler devirtualization tricks."
        ],
        "oop-abstract-interface": [
            "Abstract classes (some state) vs interfaces (pure contracts).",
            "Single class inheritance vs multiple interface implementation limits.",
            "Abstract class fields on heap vs interface constants in constant pool.",
            "Interface pollution vs abstract class code duplication.",
            "Design pattern selection (e.g. Strategy vs Template method)."
        ],
        "oop-associations": [
            "Object relationships: Association, Aggregation, Composition.",
            "Strong lifecycle dependency (Composition) vs weak reference (Aggregation).",
            "Reference pointers in garbage collection tracing roots.",
            "Cascade delete database overhead in composition hierarchies.",
            "Modeling aggregate boundaries in microservice databases."
        ],
        "oop-solid-1": [
            "Single Responsibility, Open-Closed, Liskov Substitution rules.",
            "Interface inheritance vs behavioral subtype contract checking.",
            "Abstracting runtime behaviors using polymorphism to fulfill OCP.",
            "Complexity overhead of creating multiple classes for SRP.",
            "Writing regression-free updates in large enterprise frameworks."
        ],
        "oop-solid-2": [
            "Interface Segregation and Dependency Inversion rules.",
            "Decoupled client interfaces vs fat multi-purpose interfaces.",
            "Dependency injection containers and runtime reference wiring.",
            "Performance overhead of framework-level bean scanning.",
            "Designing pluggable plugins for third-party developer platforms."
        ],
        "oop-access-mods": [
            "Private, Default, Protected, Public visibility scopes.",
            "Package-private internal safety vs public API visibility.",
            "JVM verification checks of access control during class loading.",
            "Reflection API bypassing access modifiers (using setAccessible).",
            "Encapsulating critical system variables from unauthorized extensions."
        ],
        "oop-binding": [
            "Early compile-time binding vs late runtime dynamic binding.",
            "Static/private binding paths vs virtual/interface dispatch paths.",
            "Compiler static checks and constant folding optimizations.",
            "Inlining virtual methods (devirtualization) in JIT compilers.",
            "Performance tuning of method calls in high-throughput backends."
        ],
        "oop-gc-memory": [
            "Reclaiming unused object memory automatically or manually.",
            "Reference counting loops vs tracing garbage collection roots.",
            "Generational hypothesis: dividing young Eden from tenured space.",
            "Stop-The-World latency vs memory compacting performance.",
            "Off-heap memory storage for low-latency database caching."
        ],
        "oop-copying": [
            "Copying reference addresses vs duplicating memory values.",
            "Shallow cloning reference arrays vs deep cloning instance trees.",
            "Object serialization/deserialization copies vs copy factories.",
            "Memory and CPU overhead of deep clone recursion checks.",
            "Implementing immutable state managers in reactive applications."
        ],
        "oop-copy-constructor": [
            "Initializing a new class instance from an existing instance.",
            "Deep copy constructors vs compiler-generated default copy.",
            "C++ Rule of Three (Destructor, Copy Constructor, Copy Assignment).",
            "Prevent compiler recursion by passing copy parameter by reference.",
            "Safe resource resource acquisition and release (RAII) execution."
        ]
    }
    levels = depth_levels.get(tid, [
        "Core syntax, declaration, and package compilation.",
        "Method binding parameters and return type checks.",
        "Runtime heap allocation and pointer storage mechanics.",
        "System decoupling design patterns and scaling concerns.",
        "Production runtime execution flags and memory leaks."
    ])
    return f"""
<div class="box box-depth" style="padding: 10px; margin-bottom: 0; border-left-color: #3182CE; background: #EBF8FF;">
  <div class="box-title" style="font-size: 8pt; color: #3182CE; margin-bottom: 4px;">📊 Interview Depth</div>
  <div style="font-size: 7.2pt; line-height: 1.35; color: #2D3748;">
    <strong>L1:</strong> {levels[0]}<br>
    <strong>L2:</strong> {levels[1]}<br>
    <strong>L3:</strong> {levels[2]}<br>
    <strong>L4:</strong> {levels[3]}<br>
    <strong>L5:</strong> {levels[4]}
  </div>
</div>
"""

# ─────────────────────────────────────────
# GENERATE_PAGE: 14-Section Template with Bottom Grid
# ─────────────────────────────────────────
def generate_page(topic, current_page, total_pages):
    num = topic['num']
    title = topic['title']
    subtitle = topic['subtitle']
    chapter = topic['chapter']
    left_col = topic['left_col']
    right_col = topic['right_col']
    trap = topic['trap']
    trick = topic['trick']
    tid = topic['id']
    stars = topic['yield_stars']
    
    page_indicator = f"PAGE {str(current_page).zfill(2)} / {str(total_pages).zfill(2)}"
    
    # Conditional High Yield Badge (Top 20%)
    header_right_content = """
        <div class="badge-yield">🔥 HIGH YIELD</div>
        <div class="header-badge">Placement Handbook</div>
    """ if tid in HIGH_YIELD_TOPICS else """
        <div class="header-badge">Core CS Notes</div>
    """
    
    # Space Filler Content
    space_filler = get_oop_space_filler(tid)
    
    # Extract Mistake from booster HTML using re
    import re
    booster_html = OOP_BOOSTERS.get(tid, "")
    mistake_text = "Believing that textbook definitions are sufficient; always lead with real-world trade-offs."
    
    mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*<strong>", booster_html)
    if not mistake_match:
        mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*$", booster_html)
    if mistake_match:
        mistake_text = mistake_match.group(1).replace("</p>", "").strip()
        
    followups_text = get_topic_followups(tid)
    
    industry_box = get_oop_industry_box(tid)
    depth_box = get_oop_depth_box(tid)
    left_col_updated = left_col + "\n" + industry_box + "\n" + depth_box
    
    return f"""
  <div class="page" id="{tid}">
    <!-- Header (L1) -->
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        {header_right_content}
      </div>
    </div>
 
    <!-- Topic Bar (L2) -->
    <div class="topic-bar">
      <div class="topic-bar-top">
        <div class="topic-eyebrow">{chapter}</div>
        <div class="yield-rating">Yield: <span class="stars-gold">{stars}</span></div>
      </div>
      <div class="topic-title">{num} - {title}</div>
      <div class="topic-subtitle">{subtitle}</div>
    </div>
 
    <!-- Body Container (L3) -->
    <div class="body-container">
      <!-- Left Column -->
      <div class="col-left">
        {left_col_updated}
      </div>
      
      <!-- Right Column -->
      <div class="col-right">
        {right_col}
        <!-- Space Filler replacing the old What to Say booster -->
        {space_filler}
      </div>
    </div>
 
    <!-- Bottom Placement Grid (L4) - 4-part placement section above the footer -->
    <div class="bottom-placement-grid">
      <div class="placement-block block-mistake">
        <div class="placement-block-title">⚠️ Common Mistake</div>
        <div>{mistake_text}</div>
      </div>
      <div class="placement-block block-trap">
        <div class="placement-block-title">🛑 Interviewer Trap</div>
        <div>{trap}</div>
      </div>
      <div class="placement-block block-followups">
        <div class="placement-block-title">🔄 Top Follow-Ups</div>
        <div>{followups_text}</div>
      </div>
      <div class="placement-block block-trick">
        <div class="placement-block-title">💡 Memory Trick</div>
        <div>{trick}</div>
      </div>
    </div>
    
    <!-- Footer (L5) -->
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>{title}</span></div>
      </div>
      <div class="page-number-premium">
        {page_indicator}
      </div>
    </div>
  </div>
"""

cover_page = f"""
  <div class="page cover-page" id="oop-cover">
    <div class="cover-logo-container">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
    </div>
    <div class="cover-eyebrow">Core Computer Science</div>
    <div class="cover-title">Object-Oriented<br>Programming</div>
    <div class="cover-subtitle">Placement Preparation Notes</div>
    <div style="font-size: 11pt; color: #718096; font-weight: 700; margin-top: -30px; margin-bottom: 50px;">Created by Pranav Gawai</div>
    <div class="cover-footer">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <a href="https://grindos.pranavx.in">grindos.pranavx.in</a>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# ROADMAP PAGE (Page 2)
# ─────────────────────────────────────────
roadmap_page = f"""
  <div class="page roadmap-page" id="oop-roadmap">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">OOP ROADMAP</div>
      </div>
    </div>
    
    <div style="padding: 30px 40px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 26pt; font-weight: 800; color: #111; margin-bottom: 8px;">Object-Oriented Programming Roadmap</div>
        <div style="font-size: 11pt; color: #EA763F; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Placement Preparation Guide</div>
        
        <div style="background: #FFF5F0; border-left: 5px solid #EA763F; padding: 14px 20px; border-radius: 6px; margin-bottom: 25px;">
          <strong style="color: #EA763F; font-size: 11pt; display: block; margin-bottom: 6px;">How to use this Handbook:</strong>
          <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">Object-Oriented Programming is heavily tested on polymorphism binding, access modifier scopes, SOLID principles, and lifecycle patterns (constructors/destructors). Focus on memory structures (heap vs stack, VTABLE lookups) and C++ vs Java design decisions.</p>
        </div>
 
        <div style="margin-top: 15px;">
          <div style="font-size: 12pt; font-weight: 800; color: #1A202C; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px;">🎯 Three-Phase Learning Plan</div>
          
          <div style="display: flex; gap: 15px; margin-bottom: 15px;">
            <div style="background: #EBF8FF; border: 1px solid #BEE3F8; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #3182CE; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 1</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #2B6CB0;">Classes &amp; Pillars</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Master class/object memory model, constructors, and the 4 pillars (inheritance, polymorphism, abstraction, encapsulation). (Topics 1 - 6)</p>
            </div>
            
            <div style="background: #F0FFF4; border: 1px solid #C6F6D5; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #38A169; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 2</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #276749;">Method Binding &amp; Design</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Study method operations, VTABLE dynamic dispatch, abstract interfaces, aggregation links, and SOLID guidelines. (Topics 7 - 12)</p>
            </div>
            
            <div style="background: #FFFFF0; border: 1px solid #FEFCBF; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #D69E2E; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 3</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #B7791F;">Memory &amp; Language details</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Learn access scopes, static binding resolution, garbage collection algorithms, copy patterns, and C++ copy constructors. (Topics 13 - 17)</p>
            </div>
          </div>
        </div>
      </div>
 
      <div style="border-top: 2px solid #E2E8F0; padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 8.5pt; color: #718096;">
          <strong>Target Completion:</strong> 1.5 Hours Core Study &amp; 30 Mins Self-Recall
        </div>
        <div style="font-size: 8.5pt; color: #EA763F; font-weight: 800; text-align: right; line-height: 1.3;">
          Created by Pranav Gawai<br>
          <span style="font-size: 7.5pt; color: #718096; font-weight: 500;">grindos.pranavx.in</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Roadmap</span></div>
      </div>
      <div class="page-number-premium">PAGE 02 / 28</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# DYNAMIC TABLE OF CONTENTS (Page 3)
# ─────────────────────────────────────────
toc_rows = ""
chapters_seen = {}
for t in topics:
    ch = t['chapter']
    if ch not in chapters_seen:
        chapters_seen[ch] = []
    chapters_seen[ch].append(t)
 
# Page indices: Cover = 1, Roadmap = 2, TOC = 3, content starts at 4
for ch_name, ch_topics in chapters_seen.items():
    toc_rows += f"""
    <div style="font-size: 9.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; margin-bottom: 4px;">{ch_name}</div>
    """
    for t in ch_topics:
        idx = int(t['num']) + 3
        page_str = str(idx).zfill(2)
        toc_rows += f"""
        <div style="display: flex; align-items: flex-end; margin-bottom: 4px; font-size: 9pt; font-weight: 700; color: #2D3748;">
          <a href="#{t['id']}" style="display: flex; width: 100%; align-items: flex-end; text-decoration: none; color: inherit;">
            <span style="color: #EA763F; width: 24px; font-weight: 800;">{t['num']}</span>
            <span style="background: white; padding-right: 6px;">{t['title']}</span>
            <span style="flex: 1; border-bottom: 2px dotted #CBD5E0; position: relative; top: -3px; margin: 0 4px;"></span>
            <span style="color: #718096; font-weight: 800; padding-left: 4px;">p.{page_str}</span>
          </a>
        </div>
        """

toc_page = f"""
  <div class="page toc-page" id="oop-toc">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">INDEX</div>
      </div>
    </div>
    
    <div class="toc-inner" style="padding: 20px 40px; flex:1; display:flex; flex-direction:column; justify-content:space-between; overflow:hidden; width: 100%;">
      <div>
        <div style="font-size: 20pt; font-weight: 800; color: #111; border-bottom: 4px solid #EA763F; display: inline-block; padding-bottom: 4px; margin-bottom: 6px; letter-spacing: -0.5px;">Table of Contents</div>
        <div style="font-size: 8.5pt; color: #A0AEC0; font-weight: 600; margin-bottom: 12px;">Object-Oriented Programming · Placement Preparation Handbook</div>
        
        <div style="display: flex; gap: 24px; margin-top: 10px;">
          <!-- Left Column: Core OOP Concepts & Placement Focus -->
          <div style="width: 38%; display: flex; flex-direction: column; gap: 12px;">
            <div class="box box-theory" style="padding: 10px; margin-bottom: 0;">
              <div class="box-title" style="font-size: 8.5pt; margin-bottom: 4px;">What is OOP?</div>
              <p style="font-size: 7.8pt; line-height: 1.35; color: #4A5568; margin: 0;">
                Object-Oriented Programming (OOP) is a programming paradigm structured around <strong>Objects</strong> rather than functions or logic. It models real-world entities to produce modular, maintainable, and scalable software.
              </p>
            </div>
            
            <div class="box box-depth" style="padding: 10px; margin-bottom: 0; border-left-color: #3182CE; background: #EBF8FF;">
              <div class="box-title" style="font-size: 8.5pt; color: #3182CE; margin-bottom: 4px;">The 4 Core Pillars</div>
              <div style="font-size: 7.2pt; line-height: 1.4; color: #2D3748;">
                <strong style="color: #2B6CB0;">1. Encapsulation:</strong> Hiding internal state via private variables and exposing controlled accessors.<br>
                <strong style="color: #2B6CB0;">2. Inheritance:</strong> Establishing IS-A relations to reuse behaviors and properties.<br>
                <strong style="color: #2B6CB0;">3. Polymorphism:</strong> Responding to messages differently at compile-time (overload) or runtime (override).<br>
                <strong style="color: #2B6CB0;">4. Abstraction:</strong> Defining high-level interfaces to decouple contract from execution.
              </div>
            </div>

            <div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
              <div class="box-title" style="font-size: 8.5pt; color: #B7791F; margin-bottom: 4px;">Placement Focus</div>
              <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">
                Top product-based interviewers heavily grill candidates on <strong>runtime override mechanics (VTABLE/VPTR)</strong>, constructor/destructor execution chains, <strong>SOLID principles</strong>, and avoiding diamond inheritance traps.
              </p>
            </div>
          </div>
          
          <!-- Right Column: Table of Contents Rows -->
          <div style="width: 62%; border-left: 1px solid #E2E8F0; padding-left: 20px;">
            {toc_rows}
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Index</span></div>
      </div>
      <div class="page-number-premium">PAGE 03 / 28</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# FINAL REVISION PAGE (Page 21)
# ─────────────────────────────────────────
final_revision_page = f"""
  <div class="page final-rev-page" id="oop-finalrev">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ CRAM SHEET</div>
        <div class="header-badge">OOP Final Revision</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 14px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OOP Last-Minute Revision Sheet</div>
        <div style="font-size: 9.5pt; color: #EA763F; font-weight: 700; margin-top: 4px;">Core Pillars, Binding Protocols, and SOLID Architectures</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #EA763F; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px;">⚡ THE 4 PILLARS QUICK-VIEW</strong>
          <table style="width: 100%; font-size: 8pt; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Inheritance</td><td>Code reuse via hierarchical IS-A relationships.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Polymorphism</td><td>Same signature, multiple behaviors (VTABLE override).</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Abstraction</td><td>Design contracts hiding logic (interfaces/classes).</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Encapsulation</td><td>Binding state with private scopes &amp; public accessors.</td></tr>
          </table>
        </div>
        
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #2B6CB0; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px;">📏 SOLID PRINCIPLES INDEX</strong>
          <ul style="font-size: 8pt; list-style-type: square; padding-left: 14px; line-height: 1.4; color: #4A5568;">
            <li><strong>Single Responsibility:</strong> Class does one clean task.</li>
            <li><strong>Open-Closed:</strong> Open for extension, closed to source edit.</li>
            <li><strong>Liskov Substitution:</strong> Subtypes don't break base invariants.</li>
            <li><strong>Interface Segregation:</strong> Tiny, focused interfaces.</li>
            <li><strong>Dependency Inversion:</strong> Code directly to interface templates.</li>
          </ul>
        </div>
      </div>
      
      <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; background: #FEF8F4;">
        <strong style="color: #276749; font-size: 9.5pt; display: block; margin-bottom: 6px;">💡 TOP 5 INTERVIEW CONCEPTS TO RECALL</strong>
        <ol style="font-size: 8.5pt; padding-left: 18px; line-height: 1.5; color: #2D3748;">
          <li><strong>VTABLE Resolution:</strong> C++ objects store a <code>_vptr</code> pointing to a static VTABLE of method pointers to resolve overridden functions at runtime.</li>
          <li><strong>Diamond Problem:</strong> Ambiguity resolved in C++ via virtual base inheritance, and prevented in Java by banning multiple class inheritance.</li>
          <li><strong>Aggregation vs Composition:</strong> Aggregation is a weak HAS-A link (independent lifecycles). Composition is strong, parent-owned.</li>
          <li><strong>Rule of Three (C++):</strong> Custom destructor, copy constructor, and copy assignment are required together to manage dynamic memory.</li>
          <li><strong>Copy constructor reference:</strong> Must pass by reference (e.g. <code>Box(const Box&amp; other)</code>) to prevent infinite recursion.</li>
        </ol>
      </div>

      <div style="border: 1px dashed #EA763F; border-radius: 8px; padding: 12px; background: white; text-align: center;">
        <span style="font-size: 9pt; font-weight: 800; color: #EA763F; display: block; margin-bottom: 4px;">🎯 QUICK SELF-TEST CHECKLIST</span>
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 8pt; color: #718096; font-weight: bold;">
          <span>[ ] Differentiate aggregation and composition</span>
          <span>[ ] Trace a VTABLE lookup pointer flow</span>
          <span>[ ] Explain LSP rectangle-square violation</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Cheatsheet</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">Created by Pranav Gawai</span></div>
      </div>
      <div class="page-number-premium">PAGE 21 / 28</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPARISON CHEAT SHEET PAGE (Page 22)
# ─────────────────────────────────────────
def generate_comparison_cheat_sheet(LOGO_BASE64):
    return f"""
  <div class="page" id="oop-cheatsheet-comparison">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚖️ COMPARISONS</div>
        <div class="header-badge">Cheat Sheet</div>
      </div>
    </div>
    
    <div style="padding: 12px 20px; display: flex; flex-direction: column; gap: 4px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 2px;">
        <div style="font-size: 16pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OOP Comparison Cheat Sheet</div>
        <div style="font-size: 8.5pt; color: #EA763F; font-weight: 700; margin-top: 1px;">Quick Reference Contrast Tables for Fresher Placement Interviews</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1; min-height: 0; overflow: hidden;">
        <!-- Left Column -->
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <!-- 1. Class vs Object -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #EA763F; border-bottom: 1px solid #EA763F; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Class vs Object</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Class</th><th>Object</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Nature</td><td>Logical template/blueprint</td><td>Physical instance of class</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Memory</td><td>Occupies no memory</td><td>Allocated on heap/stack</td></tr>
              <tr><td>Existence</td><td>Declared once in code</td><td>Instantiated multiple times</td></tr>
            </table>
          </div>
          
          <!-- 2. Constructor vs Destructor -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #2B6CB0; border-bottom: 1px solid #2B6CB0; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Constructor vs Destructor</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Constructor</th><th>Destructor</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Purpose</td><td>Initializes object state</td><td>Reclaims resource/memory</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Trigger</td><td>Invoked automatically at <code>new</code></td><td>Invoked at scope exit/<code>delete</code></td></tr>
              <tr><td>Syntax</td><td>Same name as class, no return</td><td>Preceded by <code>~</code> (C++ only)</td></tr>
            </table>
          </div>

          <!-- 3. Compile-Time vs Run-Time Polymorphism -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #276749; border-bottom: 1px solid #276749; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Compile-Time vs Run-Time Polymorphism</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Compile-Time</th><th>Run-Time</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Resolution</td><td>At Compile-Time</td><td>At Run-Time</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Mechanism</td><td>Method Overloading</td><td>Method Overriding</td></tr>
              <tr><td>Speed</td><td>Faster (early static binding)</td><td>Slower (indirect VTABLE jump)</td></tr>
            </table>
          </div>

          <!-- 4. Method Hiding vs Overriding -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #7B341E; border-bottom: 1px solid #7B341E; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Method Hiding vs Overriding</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Method Hiding</th><th>Overriding</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Methods</td><td>Redefines parent static method</td><td>Redefines parent instance method</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Binding</td><td>Bound statically to class</td><td>Bound dynamically to object</td></tr>
              <tr><td>Resolution</td><td>Resolved at compile-time</td><td>Resolved at runtime (VTABLE)</td></tr>
            </table>
          </div>

          <!-- 5. Heap vs Stack -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #6B46C1; border-bottom: 1px solid #6B46C1; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Heap vs Stack Memory</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Stack</th><th>Heap</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Contents</td><td>Local variables &amp; references</td><td>Actual dynamic object instance</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Access</td><td>LIFO structure, fast execution</td><td>Random access, slower pointer jump</td></tr>
              <tr><td>Lifetime</td><td>Method execution (auto pop)</td><td>Garbage collected or manual clean</td></tr>
            </table>
          </div>

          <!-- 6. Abstraction vs Encapsulation -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #9C4221; border-bottom: 1px solid #9C4221; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Abstraction vs Encapsulation</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Abstraction</th><th>Encapsulation</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Focus</td><td>WHAT an object does</td><td>HOW state is protected</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Level</td><td>Design contract interfaces</td><td>Implementation-level data shield</td></tr>
              <tr><td>Tool</td><td>Abstract classes, interfaces</td><td>Access modifiers (private)</td></tr>
            </table>
          </div>
        </div>
        
        <!-- Right Column -->
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <!-- 7. Static vs Instance Variable -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #319795; border-bottom: 1px solid #319795; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Static vs Instance Variable</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Static Variable</th><th>Instance Variable</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Ownership</td><td>Belongs to class (one copy)</td><td>Belongs to object instance (copy/obj)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Location</td><td>Metaspace / Class Area</td><td>Heap memory inside object</td></tr>
              <tr><td>Access</td><td><code>ClassName.variable</code></td><td><code>objectReference.variable</code></td></tr>
            </table>
          </div>
  
          <!-- 8. Association vs Aggregation vs Composition -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #744210; border-bottom: 1px solid #744210; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Association / Aggregation / Composition</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Type</th><th>Bond Strength</th><th>Object Lifecycles</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Association</td><td>Generic HAS-A</td><td>Independent lifecycles</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Aggregation</td><td>Weak HAS-A</td><td>Independent (Professor/Office)</td></tr>
              <tr><td>Composition</td><td>Strong HAS-A</td><td>Dependent (House/Rooms)</td></tr>
            </table>
          </div>

          <!-- 9. Shallow Copy vs Deep Copy -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #2B6CB0; border-bottom: 1px solid #2B6CB0; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Shallow Copy vs Deep Copy</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Shallow Copy</th><th>Deep Copy</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Method</td><td>Copies top references only</td><td>Recursively duplicates all nodes</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Side-effects</td><td>Changes affect cloned copy</td><td>Complete insulation from original</td></tr>
              <tr><td>Speed</td><td>Extremely fast</td><td>Slower CPU/memory overhead</td></tr>
            </table>
          </div>

          <!-- 10. Copy Constructor vs Assignment Operator -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #2C5282; border-bottom: 1px solid #2C5282; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Copy Constructor vs Assignment Operator</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Copy Constructor</th><th>Assignment Operator</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Usage</td><td>Initializes a new object</td><td>Copies state into existing object</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Syntax</td><td><code>Box b2 = b1;</code> (New declaration)</td><td><code>b2 = b1;</code> (Pre-existing object)</td></tr>
              <tr><td>Self-Check</td><td>Not needed</td><td>Must check self-assignment (<code>this == &amp;other</code>)</td></tr>
            </table>
          </div>

          <!-- 11. Interface vs Abstract Class -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 4px 6px; background: white;">
            <div style="font-size: 7.2pt; font-weight: 800; color: #4A5568; border-bottom: 1px solid #4A5568; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase;">Interface vs Abstract Class</div>
            <table style="width: 100%; font-size: 6.5pt; border-collapse: collapse; text-align: left; line-height: 1.25;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Interface</th><th>Abstract Class</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Inheritance</td><td>Multiple interface implementation</td><td>Single base class inheritance limit</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>State</td><td>Only implicit <code>static final</code> constants</td><td>Mutable fields &amp; instance variables</td></tr>
              <tr><td>Methods</td><td>Pure contracts (default/static bodies)</td><td>Abstract or concrete method blocks</td></tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Comparisons</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">Created by Pranav Gawai</span></div>
      </div>
      <div class="page-number-premium">PAGE 22 / 28</div>
    </div>
  </div>
  """

# ─────────────────────────────────────────
# EXPECTED Q&A GENERATION (Pages 23-24)
# ─────────────────────────────────────────
def generate_expected_qa_pages_new(LOGO_BASE64):
    qas = [
        {
            "q": "What is polymorphism, and how does runtime polymorphism differ from compile-time polymorphism?",
            "a": "Polymorphism means 'many forms' and allows one interface to support different actions. Compile-time polymorphism is resolved during compilation using method overloading, where methods in the same class share a name but have different parameter counts or types, allowing the compiler to bind the call statically. Runtime polymorphism is resolved during execution using method overriding, where a subclass redefines a parent method signature. When a parent reference points to a child instance, the execution environment dynamically redirects the call to the overridden subclass method by looking up its address in the object's VTABLE at runtime.",
            "keywords": ["Method Overloading", "Method Overriding", "VTABLE lookup", "Static Binding", "Dynamic Dispatch"],
            "followups": "Can static methods be overridden? What is method hiding?",
            "mistake": "Believing static polymorphism uses VTABLE lookup. VTABLEs are exclusive to dynamic runtime overriding dispatch.",
            "depth": "Analyze the CPU branch prediction penalties associated with virtual lookup cache misses."
        },
        {
            "q": "What is the Diamond Problem in multiple inheritance, and how do C++ and Java handle it differently?",
            "a": "The Diamond Problem occurs when a child class inherits from two parent classes, which both inherit from a single grandparent class. If the grandparent defines a method and both parents override it, the child class inherits duplicate method templates, causing compiler ambiguity about which version to execute. C++ allows multiple inheritance and resolves this using the virtual keyword during parent inheritance, forcing only a single grandparent instance to compile. Java avoids this completely by banning multiple class inheritance, allowing a class to implement multiple Interfaces instead, where method conflicts must be explicitly overridden by the child.",
            "keywords": ["Ambiguity Resolution", "Virtual Inheritance", "Multiple Interfaces", "Single Instance", "Diamond Path"],
            "followups": "What is a default method in Java interfaces? How are conflicts resolved?",
            "mistake": "Claiming Java doesn't support multiple inheritance at all. It supports multiple inheritance of interface types.",
            "depth": "Explain how virtual base class pointers are laid out in memory inside C++ objects."
        },
        {
            "q": "Explain the Liskov Substitution Principle (LSP) and provide a concrete example of its violation.",
            "a": "Liskov Substitution Principle, which is the 'L' in SOLID, states that objects of a superclass should be replaceable with objects of a subclass without breaking application correctness. A classic violation is modeling a Square as a subclass of a Rectangle. A Rectangle class lets you set width and height independently. However, a Square forces width and height to remain equal. If client code accepts a Rectangle reference and sets width to five and height to ten, it expects an area of fifty. If we substitute a Square, setting the height overrides the width, yielding an area of one hundred, which violates the parent contract.",
            "keywords": ["Subtype Substitutability", "Rectangle-Square", "State Invariants", "SOLID Principle", "Contract Violation"],
            "followups": "How do you refactor the Square-Rectangle design? Why is composition preferred?",
            "mistake": "Thinking LSP is violated only if the code raises a compile error. LSP violations are logical behavioral bugs.",
            "depth": "Contrast behavioral subtyping vs structural inheritance and how compiler check limits relate to them."
        },
        {
            "q": "What is the difference between an abstract class and an interface, and when would you choose one over the other?",
            "a": "An abstract class is a partial blueprint that can contain state variables, constructors, and concrete method bodies, and is inherited using single inheritance. An interface is a behavioral contract that is implicitly abstract, has no constructor, holds only static final constants, and can be implemented multiple times. I choose an abstract class when subclasses share common code and identity, establishing an 'IS-A' relationship. I choose an interface to define a decoupled capabilities contract for unrelated classes, establishing a 'CAN-DO' relationship, like making a database connector or file reader Serializable.",
            "keywords": ["State variables", "Behavior contract", "Single inheritance", "Decoupled modules", "IS-A vs CAN-DO"],
            "followups": "What is a marker interface? Why did Java 8 introduce static interface methods?",
            "mistake": "Saying interfaces cannot have method bodies. Java 8+ supports default and static interface methods.",
            "depth": "Compare performance: abstract class direct calls vs interface invokeinterface opcode lookups in the JVM."
        },
        {
            "q": "Why is composition preferred over inheritance in OOP system design?",
            "a": "Inheritance creates a tight, compile-time coupling between classes, often leading to a fragile base class problem where modifying the parent class accidentally breaks child classes. Composition, on the other hand, builds loose coupling by wrapping instances of other classes as member variables. This establishes a 'HAS-A' relationship instead of 'IS-A'. This allows us to swap behaviors dynamically at runtime using interfaces or dependency injection, and prevents deep class inheritance hierarchies that become highly complex to maintain as systems grow.",
            "keywords": ["Tight Coupling", "Loose Coupling", "Fragile Base Class", "HAS-A vs IS-A", "Runtime Strategy swapping"],
            "followups": "What is the Liskov Substitution Principle connection here? How do you implement dependency injection?",
            "mistake": "Claiming inheritance is completely obsolete. Inheritance is still appropriate for true, stable 'IS-A' hierarchies.",
            "depth": "Analyze the impact on JVM memory allocation and JIT compiler inline optimizations."
        },
        {
            "q": "What is the difference between shallow copy and deep copy, and what happens in production if we confuse them?",
            "a": "A shallow copy duplicates only the top-level object itself and copies the reference addresses of any nested objects. This means both the original and copied objects share the exact same child instances in memory, and mutating a child nested field in one object will silently modify the other object. A deep copy recursively duplicates every nested object, ensuring the copied object is completely independent. In production, using a shallow copy by mistake in state-management environments like React Redux can cause state mutations, UI rendering bugs, and database sync conflicts due to shared references.",
            "keywords": ["Reference Address Copy", "Recursive Duplication", "Shared References", "Immutable State", "State Mutation Side-Effects"],
            "followups": "How do you implement deep copy in Java? What is the cost of serialization-based deep copy?",
            "mistake": "Believing `clone()` in Java performs a deep copy by default. It performs a shallow copy unless explicitly overridden.",
            "depth": "Explain how reference loops are resolved during recursive deep copy traversals."
        }
    ]
    
    p1_html = f"""
  <div class="page" id="oop-expectedqa-new-1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 1)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[0])}
        {render_qa_block(qas[1])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 23 / 28</div>
    </div>
  </div>
  """
  
    p2_html = f"""
  <div class="page" id="oop-expectedqa-new-2">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 2)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[2])}
        {render_qa_block(qas[3])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 24 / 28</div>
    </div>
  </div>
  """

    p3_html = f"""
  <div class="page" id="oop-expectedqa-new-3">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 3)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[4])}
        {render_qa_block(qas[5])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 27 / 28</div>
    </div>
  </div>
  """
    return (p1_html + p2_html, p3_html)

def render_qa_block(item):
    kw_tags = "".join([f'<span style="background: #F7FAFC; border: 1px solid #CBD5E0; padding: 1px 6px; border-radius: 4px; font-weight: bold; font-size: 7pt; color: #4A5568; text-transform: uppercase;">{kw}</span>' for kw in item['keywords']])
    return f"""
    <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 10px 12px; background: white; display: flex; flex-direction: column; gap: 4px;">
      <div style="font-weight: 800; font-size: 9pt; color: #2B6CB0;">Q: {item['q']}</div>
      <div style="font-size: 8pt; color: #2D3748; line-height: 1.4; border-left: 3px solid #EA763F; padding-left: 8px; margin-bottom: 2px;">
        "{item['a']}"
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-top: 2px;">
        <span style="font-size: 7.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; margin-right: 4px;">Keywords:</span>
        {kw_tags}
      </div>
      <div style="font-size: 7.5pt; color: #4A5568; margin-top: 2px;">
        <strong>🔄 Follow-Up:</strong> {item['followups']}
      </div>
      <div style="font-size: 7.5pt; color: #C53030;">
        <strong>⚠️ Common Mistake:</strong> {item['mistake']}
      </div>
      <div style="font-size: 7.5pt; color: #276749;">
        <strong>📈 Expected Depth:</strong> {item['depth']}
      </div>
    </div>
"""

# ─────────────────────────────────────────
# RAPID FIRE QUESTIONS PAGE (Page 25)
# ─────────────────────────────────────────
def generate_rapid_fire_page(LOGO_BASE64):
    qas = [
        ("What is an object?", "A runtime instance of a class occupying physical memory space."),
        ("What is a class?", "A logical blueprint or user-defined type with no memory usage."),
        ("Can a constructor be virtual?", "No, constructors cannot be virtual because virtual calls require a VTABLE which is initialized by the constructor."),
        ("What is method hiding?", "Defining a static method in a subclass with the same signature as one in the parent class."),
        ("What is dynamic binding?", "Resolving method calls at runtime based on the actual object's type."),
        ("What is the diamond problem?", "Ambiguity arising from multiple inheritance when two parent classes define the same method."),
        ("What is a final class?", "A class that cannot be inherited or subclassed by any other class."),
        ("What is composition?", "A strong HAS-A relationship where child lifecycles are owned by the parent."),
        ("What is aggregation?", "A weak HAS-A relationship where children can survive parent destruction."),
        ("What are access modifiers?", "Keywords defining variable/method visibility scopes (private, default, protected, public)."),
        ("What is covariant return type?", "Allowing an overriding method to return a subtype of the parent method's return type."),
        ("What is a virtual destructor?", "A destructor ensuring the child class destructor is invoked during base-pointer deletion."),
        ("What is behavioral subtyping?", "Requiring subclasses to fulfill parent behavioral invariants, not just method signature matches."),
        ("What is an interface marker?", "An empty interface with no methods, used to tag a class as having some capability, like Cloneable."),
        ("Can static variables be GCed?", "Yes, but only when their class loader itself is garbage collected."),
        ("What is early vs late binding?", "Early resolves at compile-time (overloads); late resolves at runtime based on dynamic object type."),
        ("Virtual call in C++ constructor?", "Yes, but it resolves statically to the current class version as derived type is not yet built."),
        ("What is Fragile Base Class?", "When parent class modifications unintentionally break inherited subclasses due to tight coupling.")
    ]
    
    left_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[:9]])
    right_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[9:]])
    
    return f"""
  <div class="page" id="oop-rapidfire-page">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ RAPID FIRE</div>
        <div class="header-badge">Placement Recall</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OOP Rapid Fire Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Fast-Recall Flashcards for Last-Minute Self-Testing</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {left_col_cards}
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {right_col_cards}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 25 / 28</div>
    </div>
  </div>
"""

def render_rapid_card(q, a):
    return f"""
    <div style="border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 8px; background: white;">
      <div style="font-weight: 800; font-size: 8pt; color: #EA763F; margin-bottom: 2px;">Q: {q}</div>
      <div style="font-size: 7.5pt; color: #4A5568; line-height: 1.3;">A: {a}</div>
    </div>
"""

# ─────────────────────────────────────────
# COMMON TRAPS PAGE (Page 26)
# ─────────────────────────────────────────
def generate_common_traps_page(LOGO_BASE64):
    traps = [
        {
            "title": "Trap 1: The Virtual Constructor Myth",
            "question": "Why can't we declare a class constructor virtual in C++?",
            "intercept": "Explain that constructors create the object and initialize the virtual table pointer (_vptr). A virtual call requires the _vptr and object to already exist in memory, making virtual constructors a logical impossibility."
        },
        {
            "title": "Trap 2: The Java Interface State Trap",
            "question": "Can Java interfaces have state variables inside their definition?",
            "intercept": "No. All fields declared in an interface are implicitly public, static, and final. They are compile-time constants scoped at the class/interface level, not mutable instance state variables."
        },
        {
            "title": "Trap 3: C++ Copy Constructor Parameter Pass",
            "question": "Why must copy constructor parameters be passed by reference?",
            "intercept": "If passed by value, the compiler must copy the argument to pass it. Copying that argument invokes the copy constructor again, initiating another copy, leading to infinite compile-time recursion and stack overflow."
        },
        {
            "title": "Trap 4: Abstract Class Instantiation Check",
            "question": "Can we directly instantiate an abstract class?",
            "intercept": "No. Abstract classes are incomplete blueprints and cannot be instantiated with `new`. However, they do contain constructors, which run automatically during subclass initialization to set inherited fields."
        },
        {
            "title": "Trap 5: Overriding Static Methods Scope",
            "question": "Can static methods be overridden in Java subclasses?",
            "intercept": "No. Overriding depends on dynamic binding of object instances. Static methods are bound statically to the class name at compile-time. Redefining a static method in a subclass is Method Hiding, not overriding."
        },
        {
            "title": "Trap 6: The VTABLE Memory Overhead Trap",
            "question": "Does adding virtual methods increase the size of class instances?",
            "intercept": "No. No matter how many virtual methods are added, only a single virtual table pointer (_vptr) is added to each object instance (8 bytes on 64-bit). The VTABLE itself is shared globally at the class level in Metaspace."
        },
        {
            "title": "Trap 7: Diamond default method conflicts in Java",
            "question": "What happens if a class implements two interfaces defining default methods with identical signatures?",
            "intercept": "The compiler throws a conflict error. The class must override the conflicting method and explicitly invoke the desired version using super syntax (e.g. InterfaceName.super.methodName())."
        },
        {
            "title": "Trap 8: C++ Non-Virtual Destructor Memory Leak",
            "question": "What happens if a base class destructor is not declared virtual when deleting via a base pointer?",
            "intercept": "It triggers undefined behavior; typically, only the base destructor runs. The derived destructor is bypassed, leaking heap-allocated memory and other resource handles owned by the subclass."
        }
    ]
    
    rows = ""
    for item in traps:
        rows += f"""
        <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white; margin-bottom: 4px;">
          <div style="font-weight: 800; font-size: 8pt; color: #C53030; margin-bottom: 2px;">{item['title']}</div>
          <div style="font-size: 7.2pt; font-style: italic; color: #4A5568; margin-bottom: 2px;">Interviewer: "{item['question']}"</div>
          <div style="font-size: 7.2pt; color: #2D3748; line-height: 1.3; border-left: 2px solid #E53E3E; padding-left: 6px;">
            <strong>Deflection:</strong> {item['intercept']}
          </div>
        </div>
        """
        
    return f"""
  <div class="page" id="oop-commontraps-page">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F5; color:#E53E3E;">🛑 INTERVIEW TRAPS</div>
        <div class="header-badge">Placement Tactics</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OOP Common Traps &amp; Deflections</div>
        <div style="font-size: 9pt; color: #E53E3E; font-weight: 700;">Tactical Responses to Deflect Tricky Placement Questions</div>
      </div>
      
      <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
        {rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Common Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 26 / 28</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# BLANK NOTES PAGES (2 Pages)
# ─────────────────────────────────────────
blank_notes_pages = f"""
  <div class="page" id="oop-notes-1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">NOTES</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column;">
      <div style="font-size: 16pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 12px;">Personal Notes &amp; Scribbles</div>
      <div class="notes-lines" style="flex: 1; background-image: linear-gradient(#E2E8F0 1px, transparent 1px); background-size: 100% 24px; line-height: 24px; margin-top: 10px;"></div>
      <div style="text-align: center; margin-top: 15px; font-size: 9pt; font-weight: bold; color: #A0AEC0;">
        For practice questions and mock coding rounds, visit <a href="https://grindos.pranavx.in" style="color: #EA763F; text-decoration: none;">grindos.pranavx.in</a>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OOP <span>›</span> <span>Notes</span></div>
      </div>
      <div class="page-number-premium">PAGE 28 / 28</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPILING HTML PAGES
# ─────────────────────────────────────────
total_content_pages = len(topics)
content_pages_html = "".join([generate_page(t, i+4, 28) for i, t in enumerate(topics)])
comparison_cheat_sheet_html = generate_comparison_cheat_sheet(LOGO_BASE64)
expected_qa_p1_p2, expected_qa_p3 = generate_expected_qa_pages_new(LOGO_BASE64)
rapid_fire_html = generate_rapid_fire_page(LOGO_BASE64)
common_traps_html = generate_common_traps_page(LOGO_BASE64)

# ─────────────────────────────────────────
# CSS DESIGN SYSTEMS
# ─────────────────────────────────────────
css = f"""
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ font-family: 'DM Sans', sans-serif; background: #E5E7EB; color: #333; }}
  
  /* A4 PORTRAIT CONTAINER */
  .page {{
    width: 210mm;
    height: 297mm;
    background: #FFFFFF;
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    page-break-after: always;
    break-after: page;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    margin: 10px auto;
  }}
  
  @media print {{
    body {{ background: white; }}
    .page {{ margin: 0; box-shadow: none; page-break-after: always; break-after: page; }}
  }}
  
  /* BORDER LINE PATTERN ON ALL PAGES */
  .page::before {{
    content: "";
    position: absolute;
    top: 5mm;
    bottom: 5mm;
    left: 5mm;
    right: 5mm;
    border: 1px solid rgba(234, 118, 63, 0.15);
    pointer-events: none;
    border-radius: 4px;
    z-index: 10;
  }}
  
  /* COVER PAGE */
  .cover-page {{ justify-content: center; align-items: center; text-align: center; padding: 40px; border: 8px solid #EA763F; }}
  .cover-page::before {{ display: none; }}
  .cover-logo-container {{ width: 120px; height: 120px; margin-bottom: 40px; display: flex; justify-content: center; align-items: center; }}
  .cover-logo-container img {{ width: 100px; object-fit: contain; }}
  .cover-eyebrow {{ font-size: 14pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px; }}
  .cover-title {{ font-size: 42pt; font-weight: 800; color: #111; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1.5px; }}
  .cover-subtitle {{ font-size: 18pt; color: #666; font-weight: 600; margin-bottom: 60px; }}
  .cover-footer {{ position: absolute; bottom: 60px; font-size: 12pt; font-weight: 800; color: #888; letter-spacing: 1px; display: flex; align-items: center; gap: 12px; }}
  .cover-footer img {{ height: 24px; }}
  .cover-footer a {{ text-decoration: none; color: inherit; }}
 
  /* TOC PAGE */
  .toc-page {{ justify-content: flex-start; }}
  .toc-inner {{ padding: 30px 40px; width: 100%; }}
 
  /* HEADER */
  .header {{ background: #EA763F; height: 14mm; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; color: white; flex-shrink: 0; margin-top: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .header-left {{ display: flex; align-items: center; gap: 12px; }}
  .header-logo {{ height: 8mm; filter: brightness(0) invert(1); }}
  .header-wordmark {{ font-size: 16pt; font-weight: 800; letter-spacing: -0.5px; }}
  .header-right {{ display: flex; align-items: center; gap: 8px; }}
  .badge-yield {{ background: #FFF; color: #E53E3E; padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 8.5pt; display: flex; align-items: center; gap: 4px; }}
  .header-badge {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 10pt; }}
 
  /* TOPIC BAR */
  .topic-bar {{ padding: 10px 24px; border-bottom: 2px solid #EBE5DB; background: white; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .topic-eyebrow {{ font-size: 9pt; color: #EA763F; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }}
  .yield-rating {{ font-size: 9pt; font-weight: 800; color: #4A5568; }}
  .stars-gold {{ color: #D69E2E; font-size: 10pt; letter-spacing: 1px; }}
  .topic-title {{ font-size: 19pt; font-weight: 800; color: #111; margin-bottom: 2px; letter-spacing: -0.5px; }}
  .topic-subtitle {{ font-size: 9.5pt; color: #666; font-weight: 600; line-height: 1.3; }}
 
  /* BODY COLUMNS */
  .body-container {{ display: flex; flex: 1; overflow: hidden; min-height: 0; margin-left: 5mm; margin-right: 5mm; }}
  .col-left {{ width: 50%; background: #FEF8F4; padding: 8px 12px; border-right: 1px solid #F0E6DD; overflow: hidden; display: flex; flex-direction: column; gap: 8px; }}
  .col-right {{ width: 50%; background: #FFFFFF; padding: 8px 12px; display: flex; flex-direction: column; gap: 8px; overflow: hidden; }}
  
  /* BOXES */
  .box {{ border-radius: 8px; padding: 8px 10px; font-size: 8.5pt; line-height: 1.4; }}
  .box-title {{ font-size: 8pt; font-weight: 800; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px; }}
  .box-theory {{ border-left: 4px solid #EA763F; background: #FFF5F0; }}
  .box-theory .box-title {{ color: #EA763F; }}
  .box-industry {{ background: #FDF6E3; border: 1px solid #F5E6B3; }}
  .box-industry .box-title {{ color: #B7791F; }}
  .box-question {{ background: #EBF2F9; border: 1px solid #C5D9ED; }}
  .box-question .box-title {{ color: #2B6CB0; }}
  .box-question p {{ font-weight: 700; color: #1A365D; font-size: 9.5pt; line-height: 1.35; }}
  .box-buzzwords {{ background: #FDF2F8; border: 1px dashed #FCC2D7; }}
  .box-buzzwords .box-title {{ color: #D53F8C; margin-bottom: 4px; }}
  .buzzword-tags {{ display: flex; gap: 4px; flex-wrap: wrap; }}
  .buzz-tag {{ background: white; border: 1px solid #FCC2D7; color: #B83280; padding: 3px 6px; border-radius: 4px; font-weight: 800; font-size: 7pt; text-transform: uppercase; letter-spacing: 0.5px; }}
  .box-answer {{ background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
  .box-answer .box-title {{ color: #4A5568; }}
  
  /* NEW PLACEMENT BOOSTER BOXES */
  .box-say {{ border-left: 4px solid #38A169; background: #F0FFF4; }}
  .box-say .box-title {{ color: #38A169; }}
  .box-mistake {{ border-left: 4px solid #E53E3E; background: #FFF5F5; }}
  .box-mistake .box-title {{ color: #E53E3E; }}
  .box-depth {{ border-left: 4px solid #3182CE; background: #EBF8FF; }}
  .box-depth .box-title {{ color: #3182CE; }}
  
  /* FOLLOW-UP SUBSECTION */
  .followup-box {{ background: #F5EBFE; border: 1px solid #E9D8FD; }}
  .followup-title {{ color: #6B46C1; }}
  .followup-q {{ font-weight: 800; color: #44337A; font-size: 8.5pt; margin-bottom: 2px; }}
  .followup-q::before {{ content: "→ "; color: #805AD5; }}
  .followup-a {{ color: #553C9A; font-size: 8pt; line-height: 1.35; }}
 
  /* CONCEPT DIAGRAMS */
  .concept-visual {{ background: white; border-radius: 8px; padding: 10px; border: 1px solid #EBE5DB; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  .visual-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: center; }}
  .visual-table th {{ background: #EDF2F7; color: #4A5568; padding: 4px; border-bottom: 1.5px solid #CBD5E0; font-weight: 800; }}
  .visual-table td {{ padding: 4px; border-bottom: 1px solid #E2E8F0; }}
  
  .row-app {{ background: #FFF5F5; font-weight: bold; color: #C53030; }}
  .row-trans {{ background: #FFFFF0; font-weight: bold; color: #B7791F; }}
  .row-net {{ background: #EBF8FF; font-weight: bold; color: #2B6CB0; }}
  .row-link {{ background: #F0FFF4; font-weight: bold; color: #276749; }}
  .row-phy {{ background: #F7FAFC; font-weight: bold; color: #4A5568; }}
  
  .contrast-table td {{ font-weight: bold; }}
  .contrast-table tr:nth-child(even) {{ background: #F7FAFC; }}
  
  .flow-container {{ display: flex; flex-direction: column; width: 100%; align-items: center; justify-content: center; gap: 2px; }}
  .flow-block {{ width: 90%; text-align: center; padding: 6px; border-radius: 6px; font-size: 8pt; font-weight: 800; border: 1.5px solid; }}
  .block-orange {{ background: #FFF5F0; border-color: #EA763F; color: #EA763F; }}
  .block-blue {{ background: #EBF8FF; border-color: #3182CE; color: #3182CE; }}
  .block-green {{ background: #F0FFF4; border-color: #38A169; color: #38A169; }}
  .block-grey {{ background: #F7FAFC; border-color: #CBD5E0; color: #4A5568; }}
  .flow-arrow {{ font-size: 7pt; font-weight: bold; color: #A0AEC0; margin: 1px 0; }}
  
  .diagram-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 100%; }}
  .grid-item {{ border: 1px solid #E2E8F0; padding: 6px; border-radius: 6px; font-size: 8pt; text-align: center; background: white; }}
 
  /* NOTES LINES FOR BLANK PAGES */
  .notes-lines {{
    flex: 1;
    background-image: linear-gradient(#E2E8F0 1px, transparent 1px);
    background-size: 100% 24px;
    margin-top: 10px;
  }}
 
  /* FOOTER WITH PREMIUM PAGE NUMBERS */
  .footer {{ height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}
 
  /* BOTTOM PLACEMENT GRID (L4) */
  .bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 8px;
    padding: 10px 16px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 140px;
    max-height: 155px;
    margin-left: 5mm;
    margin-right: 5mm;
  }}
  .placement-block {{
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 8pt;
    line-height: 1.35;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .placement-block-title {{
    font-size: 7.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  .block-mistake {{ background: #FFF5F5; border-left: 3px solid #E53E3E; color: #742A2A; }}
  .block-mistake .placement-block-title {{ color: #C53030; }}
  .block-trap {{ background: #FFF5F0; border-left: 3px solid #EA763F; color: #7B341E; }}
  .block-trap .placement-block-title {{ color: #DD6B20; }}
  .block-followups {{ background: #F5EBFE; border-left: 3px solid #805AD5; color: #553C9A; }}
  .block-followups .placement-block-title {{ color: #6B46C1; }}
  .block-trick {{ background: #F0FFF4; border-left: 3px solid #38A169; color: #276749; }}
  .block-trick .placement-block-title {{ color: #2F855A; }}
"""

# Compile final template
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OOP Placement Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  {cover_page}
 
  <!-- ROADMAP PAGE -->
  {roadmap_page}
 
  <!-- TOC PAGE -->
  {toc_page}
 
  <!-- CONTENT PAGES -->
  {content_pages_html}
 
  <!-- FINAL REVISION SHEET -->
  {final_revision_page}
 
  <!-- COMPARISON CHEAT SHEET -->
  {comparison_cheat_sheet_html}
 
  <!-- EXPECTED Q&A PAGES PART 1 & 2 -->
  {expected_qa_p1_p2}
 
  <!-- RAPID FIRE PAGE -->
  {rapid_fire_html}
 
  <!-- COMMON TRAPS PAGE -->
  {common_traps_html}
 
  <!-- EXPECTED Q&A PAGE PART 3 -->
  {expected_qa_p3}
 
  <!-- BLANK NOTES PAGES -->
  {blank_notes_pages}
</body>
</html>
"""

# Write to file
os.makedirs("subjects/oops", exist_ok=True)
output_path = "subjects/oops/01_oops_notes.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Generated complete OOP Handbook with {len(topics)} topics.")
