import 'package:dio/dio.dart';
import '../models/attempt_summary_model.dart';

/// Remote DataSource pour Attempts (appels API)
abstract class AttemptsRemoteDataSource {
  /// GET /users/me/attempts
  /// 
  /// Récupère toutes les tentatives de l'utilisateur
  /// 
  /// Returns: List<AttemptSummaryModel>
  /// Throws: DioException si erreur réseau
  Future<List<AttemptSummaryModel>> getUserAttempts();
}

class AttemptsRemoteDataSourceImpl implements AttemptsRemoteDataSource {
  final Dio _dio;

  AttemptsRemoteDataSourceImpl(this._dio);

  @override
  Future<List<AttemptSummaryModel>> getUserAttempts() async {
    final response = await _dio.get('/users/me/attempts');
    
    // L'API retourne DIRECTEMENT un array
    final data = response.data as List<dynamic>;
    
    return data
        .cast<Map<String, dynamic>>()
        .map((json) => AttemptSummaryModel.fromJson(json))
        .toList();
  }
}