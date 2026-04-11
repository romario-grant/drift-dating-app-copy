from flask import request, jsonify, session
from sqlalchemy import or_
from app import create_app, db, bcrypt
from app.models import User, Profile

app = create_app()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Drift Dating API running"}), 200


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    email = (data.get("email") or "").strip().lower()
    phone_number = (data.get("phone_number") or "").strip()
    password = data.get("password") or ""

    if not email or not phone_number or not password:
        return jsonify({
            "error": "Email, phone number, and password are required."
        }), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "error": "An account with that email already exists."
        }), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        phone_number=phone_number,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.flush()

    profile = Profile(
        user_id=user.id,
        display_name=email.split("@")[0]
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully.",
        "user": {
            "id": user.id,
            "email": user.email,
            "phone_number": user.phone_number
        }
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    session["user_id"] = user.id

    return jsonify({
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200


@app.route("/me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in."}), 401

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "phone_number": user.phone_number
    }), 200


@app.route("/profile", methods=["GET"])
def get_profile():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in."}), 401

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found."}), 404

    return jsonify({
        "id": profile.id,
        "user_id": profile.user_id,
        "display_name": profile.display_name,
        "age": profile.age,
        "bio": profile.bio,
        "location": profile.location,
        "gender": profile.gender,
        "looking_for": profile.looking_for,
        "visibility": profile.visibility,
        "profile_picture": profile.profile_picture,
        "min_preferred_age": profile.min_preferred_age,
        "max_preferred_age": profile.max_preferred_age,
        "preferred_radius_km": profile.preferred_radius_km
    }), 200


@app.route("/profile", methods=["PUT"])
def update_profile():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in."}), 401

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found."}), 404

    data = request.get_json()

    display_name = data.get("display_name")
    age = data.get("age")
    bio = data.get("bio")
    location = data.get("location")
    gender = data.get("gender")
    looking_for = data.get("looking_for")
    visibility = data.get("visibility")
    profile_picture = data.get("profile_picture")
    min_preferred_age = data.get("min_preferred_age")
    max_preferred_age = data.get("max_preferred_age")
    preferred_radius_km = data.get("preferred_radius_km")

    if display_name is not None:
        profile.display_name = str(display_name).strip()

    if age is not None:
        try:
            age = int(age)
            if age < 18:
                return jsonify({"error": "Age must be at least 18."}), 400
            profile.age = age
        except ValueError:
            return jsonify({"error": "Age must be a valid number."}), 400

    if bio is not None:
        profile.bio = str(bio).strip()

    if location is not None:
        profile.location = str(location).strip()

    if gender is not None:
        profile.gender = str(gender).strip()

    if looking_for is not None:
        profile.looking_for = str(looking_for).strip()

    if visibility is not None:
        visibility = str(visibility).strip().lower()
        if visibility not in ["public", "private"]:
            return jsonify({"error": "Visibility must be 'public' or 'private'."}), 400
        profile.visibility = visibility

    if profile_picture is not None:
        profile.profile_picture = str(profile_picture).strip()

    if min_preferred_age is not None:
        try:
            profile.min_preferred_age = int(min_preferred_age)
        except ValueError:
            return jsonify({"error": "Minimum preferred age must be a valid number."}), 400

    if max_preferred_age is not None:
        try:
            profile.max_preferred_age = int(max_preferred_age)
        except ValueError:
            return jsonify({"error": "Maximum preferred age must be a valid number."}), 400

    if preferred_radius_km is not None:
        try:
            profile.preferred_radius_km = int(preferred_radius_km)
        except ValueError:
            return jsonify({"error": "Preferred radius must be a valid number."}), 400

    if (
        profile.min_preferred_age is not None
        and profile.max_preferred_age is not None
        and profile.min_preferred_age > profile.max_preferred_age
    ):
        return jsonify({
            "error": "Minimum preferred age cannot be greater than maximum preferred age."
        }), 400

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully.",
        "profile": {
            "id": profile.id,
            "user_id": profile.user_id,
            "display_name": profile.display_name,
            "age": profile.age,
            "bio": profile.bio,
            "location": profile.location,
            "gender": profile.gender,
            "looking_for": profile.looking_for,
            "visibility": profile.visibility,
            "profile_picture": profile.profile_picture,
            "min_preferred_age": profile.min_preferred_age,
            "max_preferred_age": profile.max_preferred_age,
            "preferred_radius_km": profile.preferred_radius_km
        }
    }), 200


@app.route("/profiles", methods=["GET"])
def get_profiles():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in."}), 401

    query = Profile.query.filter(
        Profile.user_id != user_id,
        Profile.visibility == "public"
    )

    search = request.args.get("search")
    location = request.args.get("location")
    min_age = request.args.get("min_age")
    max_age = request.args.get("max_age")
    gender = request.args.get("gender")
    looking_for = request.args.get("looking_for")

    if search:
        search = search.strip()
        query = query.filter(
            or_(
                Profile.display_name.ilike(f"%{search}%"),
                Profile.bio.ilike(f"%{search}%")
            )
        )

    if location:
        query = query.filter(Profile.location.ilike(f"%{location.strip()}%"))

    if min_age:
        try:
            query = query.filter(Profile.age >= int(min_age))
        except ValueError:
            return jsonify({"error": "min_age must be a valid number."}), 400

    if max_age:
        try:
            query = query.filter(Profile.age <= int(max_age))
        except ValueError:
            return jsonify({"error": "max_age must be a valid number."}), 400

    if gender:
        query = query.filter(Profile.gender.ilike(gender.strip()))

    if looking_for:
        query = query.filter(Profile.looking_for.ilike(looking_for.strip()))

    profiles = query.all()

    results = []
    for profile in profiles:
        results.append({
            "id": profile.id,
            "user_id": profile.user_id,
            "display_name": profile.display_name,
            "age": profile.age,
            "bio": profile.bio,
            "location": profile.location,
            "gender": profile.gender,
            "looking_for": profile.looking_for,
            "visibility": profile.visibility,
            "profile_picture": profile.profile_picture,
            "min_preferred_age": profile.min_preferred_age,
            "max_preferred_age": profile.max_preferred_age,
            "preferred_radius_km": profile.preferred_radius_km
        })

    return jsonify(results), 200


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200


if __name__ == "__main__":
    app.run(debug=True)