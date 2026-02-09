import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../../auth/presentation/bloc/auth_bloc.dart';
import '../../../auth/presentation/bloc/auth_state.dart';
import '../bloc/category_bloc.dart';
import '../bloc/category_event.dart';
import '../bloc/category_state.dart';
import '../widgets/category_card.dart';
import '../../domain/entities/category_entity.dart';

/// Homepage = liste des catégories (utilisée comme Home de l'app mobile)
class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late CategoryBloc _bloc;

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final categoryBloc = BlocProvider.of<CategoryBloc>(context);

      if (categoryBloc.state is CategoryInitial) {
        debugPrint('🔄 HomePage: Chargement initial des catégories...');
        categoryBloc.add(const FetchCategories(isActive: true));
      } else {
        debugPrint('✅ HomePage: Catégories déjà en cache');
      }
    });
  }

  Future<void> _refresh() async {
    debugPrint('🔄 HomePage: Refresh manuel des catégories...');
    _bloc.add(const FetchCategories(isActive: true));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.error;
    final textSecondaryColor =
        isDarkMode ? AppColors.darkTextSecondary : AppColors.textSecondary;
    final greyColor = isDarkMode ? AppColors.grey600 : AppColors.grey400;

    return Scaffold(
      appBar: AppBar(
        title: BlocBuilder<AuthBloc, AuthState>(
          builder: (context, state) {
            final name = state is Authenticated ? state.user.name : 'Invité';
            final onPrimaryColor = colorScheme.onPrimary;

            return Text(
              'Bonjour, $name 👋',
              style: TextStyle(color: onPrimaryColor),
            );
          },
        ),
        backgroundColor: primaryColor,
        foregroundColor: colorScheme.onPrimary,
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        color: primaryColor,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8),
          child: BlocBuilder<CategoryBloc, CategoryState>(
            builder: (context, state) {
              if (state is CategoryLoading || state is CategoryInitial) {
                return Center(
                  child: Image.asset(
                    'assets/animations/loading.gif',
                    width: 64,
                    height: 64,
                    fit: BoxFit.contain,
                    color: primaryColor,
                  ),
                );
              }

              if (state is CategoryError) {
                return Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.error_outline,
                        size: 64,
                        color: errorColor,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'Erreur',
                        style: context.textTheme.headlineSmall?.copyWith(
                          color: colorScheme.onSurface,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        state.message,
                        textAlign: TextAlign.center,
                        style: context.textTheme.bodyMedium?.copyWith(
                          color: textSecondaryColor,
                        ),
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: _refresh,
                        child: const Text('Réessayer'),
                      ),
                    ],
                  ),
                );
              }

              if (state is CategoriesLoaded) {
                final categories = state.categories;
                if (categories.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.category_outlined,
                          size: 80,
                          color: greyColor,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Aucune catégorie disponible',
                          style: context.textTheme.titleLarge?.copyWith(
                            color: textSecondaryColor,
                          ),
                        ),
                      ],
                    ),
                  );
                }

                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 8.0),
                      child: Text(
                        'Quiz disponibles',
                        style: context.textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: colorScheme.onSurface,
                        ),
                      ),
                    ),
                    Expanded(
                      child: ListView.separated(
                        itemCount: categories.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 8),
                        itemBuilder: (context, index) {
                          final CategoryEntity cat = categories[index];
                          return CategoryCard(
                            category: cat,
                            onTap: () => context.push('/category/${cat.id}'),
                          );
                        },
                      ),
                    ),
                  ],
                );
              }

              return const SizedBox.shrink();
            },
          ),
        ),
      ),
    );
  }
}
